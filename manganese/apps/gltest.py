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

import os.path

import pygame

import OpenGL

OpenGL.FULL_LOGGING = True
OpenGL.ERROR_ON_COPY = True
OpenGL.FORWARD_COMPATIBLE_ONLY = True

from OpenGL import GL
from OpenGL.arrays import vbo

import OpenGL.GL.shaders

import numpy

import _apps

from manganese.vismut import gl

import manganese.vismut.gl.util
import manganese.vismut.gl.context
import manganese.vismut.gl.shaders


class Application(_apps.Application):
    max_fps = 60

    def compile_shader(self, name, type):
        with open(self.data(gl.shaders.filename(name, type),
                            app='vismut')) as shader:
            return gl.shaders.compile_shader(shader.read(), type)

    def compile_program(self, name):
        vertex = self.compile_shader(name, gl.shaders.VERTEX)
        fragment = self.compile_shader(name, gl.shaders.FRAGMENT)

        return GL.shaders.compileProgram(vertex, fragment)

    def setup(self):
        self.program = self.compile_program('simple')

        self.vbo = vbo.VBO(numpy.array([
            [0, 1, 0],
            [-1, -1, 0],
            [1, -1, 0],
            [2, -1, 0],
            [4, -1, 0],
            [4, 1, 0],
            [2, -1, 0],
            [4, 1, 0],
            [2, 1, 0],
            ], 'f'))

        self.matrix = numpy.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 8],
            ], 'f')

    def render(self):
        print self.context.clock.get_fps()
        with gl.util.enable(GL.GL_PROGRAM_POINT_SIZE):
            with gl.util.enable(GL.GL_POINT_SMOOTH):
                with gl.util.use_program(self.program) as program:
                    gl.util.transformation_matrix(program, self.matrix)

                    with gl.util.bind(self.vbo):
                        with gl.util.enable_client_state(GL.GL_VERTEX_ARRAY):
                            GL.glVertexPointerf(self.vbo)
                            GL.glDrawArrays(GL.GL_POINTS, 0, 9)

    def run(self):
        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps)
        self.context.setup(self.cfg('mode', '640x480'))
        self.setup()

        self.context.run()
