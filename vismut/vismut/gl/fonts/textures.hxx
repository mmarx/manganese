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

#ifndef VISMUT_GL_FONTS_TEXTURES_HXX
#define VISMUT_GL_FONTS_TEXTURES_HXX

#include <string>

#include <boost/python.hpp>

#include "faces.hxx"

namespace bi
{
  namespace py = boost::python;

  void
  init_numpy ();

  py::object
  make_font_texture (FT_Library library,
		     std::string filename,
		     unsigned long face,
		     unsigned int size);
}

#endif // VISMUT_GL_FONTS_TEXTURES_HXX
