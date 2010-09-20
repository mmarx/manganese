# mutabor-ng platform
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

function(python_extension extension_NAME extension_PREFIX install_PREFIX)
  set(impure TRUE)
  foreach(arg ${ARGN})
    if(${arg} STREQUAL "PURE")
      set(impure FALSE)
    endif(${arg} STREQUAL "PURE")
  endforeach(arg)

  # find source files
  file(GLOB ${extension_NAME}_SOURCES ${extension_PREFIX}/*.cxx)
  file(GLOB ${extension_NAME}_PYTHON ${extension_PREFIX}/*.py)

  # build the extension, if necessary
  if(impure)
    add_library(${extension_NAME} MODULE ${${extension_NAME}_SOURCES})
    target_link_libraries(${extension_NAME} ${Boost_PYTHON_LIBRARY})
    set_target_properties(${extension_NAME} PROPERTIES PREFIX "_")

    # install it
    install(TARGETS ${extension_NAME} LIBRARY DESTINATION ${install_PREFIX}${extension_PREFIX})
  endif(impure)

  # install the python part
  install(FILES ${${extension_NAME}_PYTHON} DESTINATION ${install_PREFIX}${extension_PREFIX})
endfunction(python_extension)