
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
            [.125, 0, 0, 0],
            [0, .125, 0, 0],
            [0, 0, .125, 0],
            [0, 0, 0, 1],
            ], 'f')

    def render(self):
        GL.glUseProgram(self.program)
        loc = GL.glGetUniformLocation(self.program, "transformation")
        GL.glUniformMatrix4fv(loc, 1, True, self.matrix)
        try:
            self.vbo.bind()
            try:
                GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
                GL.glVertexPointerf(self.vbo)
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, 9)
            finally:
                self.vbo.unbind()
                GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        finally:
            GL.glUseProgram(0)

    def run(self):
        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps)
        self.context.setup(self.cfg('mode', '640x480'))
        self.setup()

        self.context.run()
