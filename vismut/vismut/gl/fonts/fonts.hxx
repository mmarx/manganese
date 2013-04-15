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

#ifndef VISMUT_GL_FONTS_FONTS_HXX
#define VISMUT_GL_FONTS_FONTS_HXX

#include <memory>
#include <string>
#include <exception>

#include <boost/python.hpp>

#include <ft2build.h>
#include FT_FREETYPE_H

#include "errors.hxx"

namespace bi
{
  namespace py = boost::python;

  inline void
  check (FT_Error error)
    throw (std::runtime_error)
  {
    if (!error)
      {
	return;
      }

    throw std::runtime_error ("FreeType error: " + error_map[error]);
  }


  py::object
  make_font_texture (FT_Library library,
		     std::string filename,
		     unsigned long face,
		     unsigned int size);

  class
  FreeType
  {
  public:
    FreeType ()
    {
      check (FT_Init_FreeType (&library_));
    }

    ~FreeType ()
    {
      check (FT_Done_FreeType (library_));
    }

    FT_Library
    get ()
    {
      return library_;
    }

    py::object
    font_texture (std::string filename,
		  unsigned long face,
		  unsigned int size)
    {
      return make_font_texture (library_, filename, face, size);
    }

  private:
    FT_Library library_;
  };
}

#endif // VISMUT_GL_FONTS_FONTS_HXX
