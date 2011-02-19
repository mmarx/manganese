
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


class Shaders(object):
    VERTEX, FRAGMENT = range(2)

    exts = {VERTEX: 'vert',
            FRAGMENT: 'frag',
            }

    types = {VERTEX: GL.GL_VERTEX_SHADER,
             FRAGMENT: GL.GL_FRAGMENT_SHADER,
             }

    @classmethod
    def filename(cls, basename, type):
        return '%s.%s' % (basename, cls.exts[type])

    @classmethod
    def compile(cls, shader, type):
        return GL.shaders.compileShader(shader, cls.types[type])


class Application(_apps.Application):
    max_fps = 60

    def compile_shader(self, name, type):
        with open(self.data(Shaders.filename(name, type),
                            app='vismut')) as shader:
            return Shaders.compile(shader.read(), type)

    def compile_program(self, name):
        vertex = self.compile_shader(name, Shaders.VERTEX)
        fragment = self.compile_shader(name, Shaders.FRAGMENT)

        return GL.shaders.compileProgram(vertex, fragment)

    def setup(self):
        pygame.init()

        flags = pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF

        self.screen = pygame.display.set_mode((640, 480), flags)
        self.clock = pygame.time.Clock()

        self.running = True

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
        self.setup()

        while self.running:
            self.clock.tick(self.max_fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.render()

            pygame.display.flip()
