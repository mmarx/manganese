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
    vertices = [[(1 + 0.5 * v * cos(0.5 * u)) * cos(u),
                 (1 + 0.5 * v * cos(0.5 * u)) * sin(u),
                 0.5 * v * sin(0.5 * u)]
                for u in numpy.linspace(0, 2 * pi, steps)
                for v in [-1, 1,]]

    return vertices

class Application(molybdenum.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self._geometry('moebius', moebius(steps=2500))
        self.the_matrix = gl.util.ortho(-5, 5, -5, 5, -5, 5)

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        with gl.util.use_program(self.programs['flat']) as program:
            gl.util.transformation_matrix(program, self.the_matrix,
                                          location=self._loc('flat',
                                                             'transformation'))

            with gl.util.draw_vbo(0, self.vbos['moebius']):
                GL.glUniform3f(self._loc('flat', 'translation'), 0.0, 0.0, 0.0)
                GL.glUniform4f(self._loc('flat', 'color'),
                               0.0, 0.0, 0.0, 1.0)
                #*self._color('key', 'bg', 'anchor_initial'))
                GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertices['moebius'])
