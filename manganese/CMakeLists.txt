######################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011 Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
######################################################################


# manganese-runner and top-level python module tree
file(GLOB manganese_SOURCES *.cxx)
file(GLOB manganese_PYTHON *.py)

configure_file(config.hxx.in config.hxx ESCAPE_QUOTES)
include_directories(${CMAKE_CURRENT_BINARY_DIR})

add_executable(mng ${manganese_SOURCES})
target_link_libraries(mng ${Boost_LIBRARIES})
target_link_libraries(mng ${PYTHON_LIBRARIES})
install(TARGETS mng RUNTIME DESTINATION .)
install(FILES ${manganese_PYTHON} DESTINATION manganese)

# find JACK
find_package(Jack)

include(PythonExtension)

python_extension(config "config/" "manganese/" PURE)
python_extension(apps "apps/" "manganese/" PURE)
python_extension(_apps "apps/_apps" "manganese/" PURE)
python_extension(math "math/" "manganese/" PURE)
python_extension(midi "midi/" "manganese/" PURE)
python_extension(jack "midi/jack/" "manganese/")

target_link_libraries(jack ${JACK_LIBRARIES})
target_link_libraries(jack ${Boost_THREAD_LIBRARY})
