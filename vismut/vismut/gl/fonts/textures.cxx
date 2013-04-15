/***********************************************************************
 * manganese - midi analysis & visualization platform
 * Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
 * 
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301 USA.
 **********************************************************************/

#include <Python.h>
#include <numpy/arrayobject.h>

#include <iostream>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "textures.hxx"

namespace bi
{
  void
  init_numpy ()
  {
    import_array ();
  }

  void
  render (Face& face,
	  long charcode,
	  unsigned char* dst,
	  unsigned int width,
	  unsigned int height,
	  unsigned int stride)
  {
    check (FT_Load_Char (face.get (), charcode, FT_LOAD_RENDER));

    FT_GlyphSlot slot = face.get ()->glyph;

    int offset = ((height - slot->bitmap_top) * stride
		  + slot->bitmap_left) * 0;

    for (int y = slot->bitmap.rows; y > 0; --y)
      {
	for (int x = 0; x < slot->bitmap.width; ++x)
	  {
	    dst[offset + x + stride * y] =
	      slot->bitmap.buffer[x +slot->bitmap.pitch *
				  (slot->bitmap.rows - y)];
	  }
      }
  }

  void advance (int& x,
		int& y)
  {
	if (++x >= 8)
	  {
	    ++y;
	    x = 0;
	  }
  }

  void
  render_range (Face& face,
		long from,
		long to,
		unsigned char* dst,
		unsigned int width,
		unsigned int height,
		unsigned int size,
		int& x,
		int& y)
  {
    for (long c = from; c <= to; ++c)
      {
	render (face,
		c,
		dst + x * width + y * size * height,
		width,
		height,
		size);
	advance (x, y);
      }
  }

  py::object
  make_font_texture (FT_Library library,
		     std::string filename,
		     unsigned long the_face,
		     unsigned int size)
  {
    Face face (library, filename, the_face);

    npy_intp shape[] = { size,
			 size };

    py::object array;

    PyArray_Descr* descr = PyArray_DescrFromType (PyArray_UBYTE);
    py::handle<> the_array (PyArray_Zeros (2, shape, descr, 0));

    unsigned char* data = reinterpret_cast<unsigned char*>
      (reinterpret_cast<PyArrayObject*> (the_array.get ())->data);

    int x = 0;
    int y = 0;
    int stride = size / 8;

    face.size (stride, stride);

    render_range (face, 'A', 'Z', data, stride, stride, size, x, y);
    render_range (face, 'a', 'z', data, stride, stride, size, x, y);
    render_range (face, '0', '9', data, stride, stride, size, x, y);
    render_range (face, '+', '+', data, stride, stride, size, x, y);
    render_range (face, '-', '-', data, stride, stride, size, x, y);

    array = py::object (the_array);

    return array;
  }
}
