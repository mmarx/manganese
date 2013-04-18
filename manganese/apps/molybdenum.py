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

import vismut


class Net(centered_net.ToneNet):
    pass

class Application(vismut.Application):
    max_fps = 60
    data_suffix = 'vismut'

    def render(self):
        super(Application, self).render

    def run(self):
        self.action = 'live'
        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps,
                                                vsync=self.vsync)
        mode = self.cfg('mode', (640, 480))
        self.context.setup(mode)
        self.aspect = mode[0] / mode[1]

        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)
        self.font_atlas = gl.textures.font_atlas(self.data('vera.ttf'),
                                                 0, 128)
        self.theme = themes.get(self.cfg('theme', 'default'), self)
        self.tn = Net(left=-3, right=2, top=3, bottom=-2)
        self.resize_net()

        self.init_gl()

        self.context.add_handler(pygame.VIDEORESIZE, self.resize_event)

        self.context.run()

        self.cleanup_gl()

        return

        auto = self.cfg('connect', [])
        with midi.jack.create_client(autoconnect = au) as client:

            while True:
                client.check_auto_connect()

                if client.have_events:
                    event = client.next_event()
                    print event, ": ", repr(event)
