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

from __future__ import division

from math import sin, cos, pi

import numpy
import pygame
import pygame.image

import OpenGL

OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True
OpenGL.FULL_LOGGING = False
OpenGL.ERROR_ON_COPY = True
OpenGL.FORWARD_COMPATIBLE_ONLY = True

from OpenGL import GL
from OpenGL.arrays import vbo

import _apps

from manganese.vismut import gl
from manganese.vismut import themes
from manganese.utabor import centered_net

import manganese.vismut.gl.util
import manganese.vismut.gl.context
import manganese.vismut.gl.shaders
import manganese.vismut.gl.geometry
import manganese.vismut.gl.textures
import manganese.midi as midi
import manganese.midi.jack

from manganese.midi.jack.event import event_from_dword

import vismut
import molybdenum

from molybdenum import MoebiusNet, MoebiusUT

def moebius(width=1, steps=100, z=0.0):
    urange = numpy.linspace(0, 2 * pi, steps)
    vertices = [[(1 + 0.5 * v * cos(0.5 * u)) * cos(u),
                 (1 + 0.5 * v * cos(0.5 * u)) * sin(u),
                 0.5 * v * sin(0.5 * u),
                 1 * u / urange[-1],
                 0.5 + 0.5 * v]
                for u in urange
                for v in [-1, 1,]]

    return vertices

class Application(molybdenum.Application):
    def __init__(self, *args, **kwargs):
        self.default_net['left'] = -6
        super(Application, self).__init__(*args, **kwargs)
        self._geometry('moebius', moebius(steps=2500))
        self.the_matrix = gl.util.ortho(-1.25 , 1.75, -1.5, 1.5, -2.5, 2.5)

    def cfg(self, key, default):
        if key == 'grow':
            return False
        return super(Application, self).cfg(key, default)

    def run(self):
        super(Application, self).run()

    def init_gl(self):
        super(Application, self).init_gl()

        tex = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
        for wrap in [GL.GL_TEXTURE_WRAP_S, GL.GL_TEXTURE_WRAP_T]:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, wrap, GL.GL_REPEAT)
        for filt in [GL.GL_TEXTURE_MIN_FILTER, GL.GL_TEXTURE_MAG_FILTER]:
            GL.glTexParameteri(GL.GL_TEXTURE_2D, filt, GL.GL_NEAREST)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA,
                        self.mode[0], self.mode[1], 0,
                        GL.GL_BGRA, GL.GL_UNSIGNED_BYTE, None)
        self.render_target = tex

    def cleanup_gl(self):
        GL.glDeleteTextures(numpy.array([self.render_target], 'uint32'))
        super(Application, self).cleanup_gl()

    def render(self):
        with gl.textures.render_to_texture(self.render_target):
            GL.glClearColor(*self.theme.color('screen', 'bg'))
            super(Application, self).render()

        GL.glClearColor(*self.theme.color('screen', 'fg'))
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with gl.util.use_program(self.programs['textured']) as program:
            gl.util.transformation_matrix(program, self.the_matrix,
                                          location=self._loc('textured',
                                                             'transformation'))
            with gl.util.draw_vbo(0, self.vbos['moebius'], stride=20):
                GL.glUniform3f(self._loc('textured', 'translation'),
                               0.0, 0.0, 0.0)
                GL.glUniform1i(self._loc('textured', 'texture'), 0)
                loc = self._loc('textured', 'tex_coords')
                with gl.util.vertex_attrib_array(loc):
                    GL.glVertexAttribPointer(loc, 2, GL.GL_FLOAT, False,
                                             20, self.vbos['moebius'] + 12)
                    GL.glBindTexture(GL.GL_TEXTURE_2D, self.render_target)
                    GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0,
                                    self.vertices['moebius'])
