# manganese - mutabor-ng platform runner
# Copyright (c) 2010, 2011, Maximilian Marx <mmarx@wh2.tu-dresden.de>
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
python_extension(midi "midi/" "manganese/" PURE)
python_extension(jack "midi/jack/" "manganese/")
python_extension(event "midi/event/" "manganese/")

target_link_libraries(jack ${JACK_LIBRARIES})
target_link_libraries(jack ${Boost_THREAD_LIBRARY})