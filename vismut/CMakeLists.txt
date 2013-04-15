########################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
########################################################################


# find FreeType
find_package(Freetype REQUIRED)
include_directories(${FREETYPE_INCLUDE_DIRS})

include(PythonExtension)

python_extension(vismut "vismut/" "manganese/" PURE)
python_extension(gl "vismut/gl/" "manganese/" PURE)
python_extension(themes "vismut/themes/" "manganese/" PURE)
python_extension(fonts "vismut/gl/fonts" "manganese/")

target_link_libraries(fonts ${FREETYPE_LIBRARIES})

file(GLOB VISMUT_DATA data/*.vert data/*.frag data/*.ttf)
install(FILES ${VISMUT_DATA} DESTINATION data/vismut/)
