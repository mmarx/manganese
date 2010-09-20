# vismut - mutabor-ng platform visualization
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

# find SDL

set(SDL_BUILDING_LIBRARY ON)
find_package(SDL REQUIRED)
find_package(OpenGL REQUIRED)

include_directories(${SDL_INCLUDE_DIR})
include_directories(${OpenGL_INCLUDE_DIR})

include(PythonExtension)

python_extension(vismut "vismut/" "manganese/")
python_extension(video "vismut/video/" "manganese/")

target_link_libraries(video ${SDL_LIBRARY})
#target_link_libraries(vismut ${OpenGL_gl_LIBRARIES})