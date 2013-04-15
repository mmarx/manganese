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

#include <boost/python.hpp>

#include "fonts.hxx"
#include "faces.hxx"

namespace bi
{
  FreeType*
  init_freetype ()
  {
    build_error_map ();
    return new FreeType ();
  }

  void
  destroy_freetype (std::auto_ptr<FreeType> library)
  {
    library.reset ();
  }

  BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(face_size_overloads,
					 size, 1, 2);

  BOOST_PYTHON_MODULE (_fonts)
  {
    using namespace boost::python;

    init_numpy ();

    def ("init_freetype",
	 init_freetype,
	 return_value_policy<manage_new_object> ());
    def ("destroy_freetype",
	 destroy_freetype);

    class_<FreeType> ("FreeType", no_init)
      .def ("make_font_texture", &FreeType::font_texture);
  }
}
