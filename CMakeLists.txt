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



project(manganese)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)

# find python
set(CMAKE_PYTHON_VERSIONS 2.6)
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

# find boost
set(BOOST_MULTITHREADED ON)
set(BOOST_USE_STATIC_LIBS OFF)
set(BOOST_ADDITIONAL_VERSIONS "1.42" "1.42.0")

find_package(Boost 1.42.0 REQUIRED COMPONENTS python program_options thread)
include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(manganese)
add_subdirectory(lithium)
add_subdirectory(caesium)
add_subdirectory(carbon)
add_subdirectory(vismut)
add_subdirectory(utabor)
