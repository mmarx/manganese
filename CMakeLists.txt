# manganese - mutabor-ng platform
# Copyright (c) 2010, Maximilian Marx <mmarx@wh2.tu-dresden.de>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

project(manganese)
cmake_minimum_required(VERSION 2.8)

set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)

# find python
set(CMAKE_PYTHON_VERSIONS 2.6)
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

# find boost
set(BOOST_MULTITHREADED OFF)
set(BOOST_USE_STATIC_LIBS OFF)
set(BOOST_ADDITIONAL_VERSIONS "1.42" "1.42.0")

find_package(Boost 1.42.0 REQUIRED COMPONENTS python program_options thread)
include_directories(${Boost_INCLUDE_DIRS})

add_subdirectory(manganese)
add_subdirectory(vismut)