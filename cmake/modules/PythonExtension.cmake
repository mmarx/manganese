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