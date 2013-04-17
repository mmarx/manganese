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

from OpenGL import GL

from manganese.vismut import gl

import manganese.vismut.gl.shaders


class GLShaderMixin(object):
    def compile_shader(self, name, type):
        with open(self.data(gl.shaders.filename(name, type))) as shader:
            return gl.shaders.compile_shader(shader.read(), type)

    def compile_program(self, name):
        vertex = self.compile_shader(name, gl.shaders.VERTEX)
        fragment = self.compile_shader(name, gl.shaders.FRAGMENT)

        return GL.shaders.compileProgram(vertex, fragment)
