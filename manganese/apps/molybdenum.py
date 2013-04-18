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

import manganese.midi as midi
import manganese.midi.jack


class Application(_apps.Application):
    max_fps = 60

    def setup(self):
        pass

    def render(self):
        pass

    def run(self):
        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps)
        self.context.setup(self.cfg('mode', '640x480'))
        self.setup()

        self.context.run()

        return

        auto = self.cfg('connect', [])
        with midi.jack.create_client(autoconnect = auto) as client:

            while True:
                client.check_auto_connect()

                if client.have_events:
                    event = client.next_event()
                    print event, ": ", repr(event)
