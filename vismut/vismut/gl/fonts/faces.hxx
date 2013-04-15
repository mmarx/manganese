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

#ifndef VISMUT_GL_FONTS_FACES_HXX
#define VISMUT_GL_FONTS_FACES_HXX

#include <string>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "fonts.hxx"
#include "textures.hxx"

namespace bi
{
  class Face
  {
  public:
    Face (FT_Library library,
	  std::string filename,
	  unsigned long face = 0)
    {
      check (FT_New_Face (library,
			  filename.c_str (),
			  face,
			  &face_));
    }

    ~Face()
    {
      check (FT_Done_Face (face_));
    }

    FT_Face
    get ()
    {
      return face_;
    }

    void
    size (long height,
	  long width = 0)
    {
      check (FT_Set_Pixel_Sizes (face_,
				 width,
				 height));
    }

  protected:
    FT_Face face_;
  };
}

#endif // VISMUT_GL_FONTS_FACES_HXX
