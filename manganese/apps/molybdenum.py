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

from manganese.midi.jack.event import event_from_dword

import vismut


class MoebiusNet(centered_net.ToneNet):
    coords = {0: (0, 0),        # C
              2: (2, 4),        # D
              4: (4, 1),        # E
              5: (6, 5),        # F
              7: (1, 2),        # G
              9: (3, 6),        # A
              11: (5, 3),       # B
          }
    offset = 0

    def name(self, x, y):
        base = x + 4 * y

        while base < -1:
            base += 7

        while base > 5:
            base -= 7

        return self._name(base, 0)

    def should_grow(self, *args, **kwargs):
        ax, ay = self.anchor

        return min(ax - self.left - 1,
                   self.right - ax) < 0

    def grow(self, min_dist=0, by=2):
        ax, ay = self.anchor

        dist = ax - 1 - self.left
        if dist < min_dist:
            self.left -= max(by, min_dist - dist)

        dist = self.right - ax
        if dist < min_dist:
            self.right += max(by, min_dist - dist)

    def pitch_coordinates(self, pitch, relative=False):
        ax, ay = self.anchor
        dx, dy = self.coords[pitch % 12]

        ox = ax
        if relative:
            ax, ay = 0, 0

        return [(ax - 1, (dy - (2 * (ox - 1))) % 7),
                (ax, (dy - (2 * ox)) % 7),
            ]

    def move(self, pitch):
        ax, ay = self.anchor
        dx, dy = self.coords[pitch % 12]

        if ax % 7 == 0:
            if dx < ax:
                self.offset = ax + 7
            elif dx > ax:
                self.offset = ax - 7

        self.anchor = (self.offset + dx % 7, ay)

    def set_active(self, keys):
        self.active = []
        for key in keys:
            self.active.extend(self.pitch_coordinates(key))


class MoebiusUT(object):
    anchor = 60
    last_anchor = 60
    keys = []
    pitch_filter = [0, 2, 4, 5, 7, 9, 11]
    patterns = {0: [0, 4, 7],
                2: [2, 5, 9],
                4: [4, 7, 11],
                5: [0, 5, 9],
                7: [2, 7, 11],
                9: [0, 4, 9],
                11: [2, 5, 11],
            }
    anchor_idx = {0: 0,
                  2: 0,
                  4: 0,
                  5: 1,
                  7: 1,
                  9: 2,
                  11: 2,
                  }

    def handle_midi(self, dword):
        event = event_from_dword(dword)
        type = event.describe_type()
        update_anchor = False

        if type in ['note on', 'note off']:
            pitch = event.raw[1]
            if pitch % 12 in self.pitch_filter:
                if type == 'note on':
                    if not update_anchor and len(self.keys) < 3:
                        update_anchor = True
                    self.keys.append(pitch)
                else:
                    if not update_anchor and pitch == self.anchor:
                        update_anchor = True
                    try:
                        self.keys.remove(pitch)
                    except ValueError:
                        print ('-!- trying to remove pitch %0xd, but it '
                               'is already gone' % pitch)

        if not update_anchor:
            return

        fst = lambda p: p[0]
        pitches = [(key % 12, key) for key in set(self.keys)]
        pitches.sort(key=fst)

        if len(pitches) < 3:
            return

        for idx in range(0, len(pitches)):
            for pattern in self.patterns:
                chord = [fst(pitch) for pitch in pitches[idx:(idx + 3)]]
                if  chord == self.patterns[pattern]:
                    anchor = pitches[idx + self.anchor_idx[pattern]][1]
                    if anchor != self.anchor:
                        self.last_anchor = self.anchor
                        self.anchor = anchor
                    return

    @property
    def anchor_changed(self):
        return self.anchor != self.last_anchor


class Application(vismut.Application):
    max_fps = 60
    data_suffix = 'vismut'
    action = 'live'
    default_net = {'left': -14,
                   'right': 0,
                   'top': 6,
                   'bottom': 0,
               }

    def render(self):
        super(Application, self).render()

    def run(self):
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
        self.theme.draw_cage = lambda: None
        self.classifier = getattr(manganese.midi.pitch,
                                  'Naming' + self.cfg('naming', 'DE'))()
        self.tn = MoebiusNet(classifier=self.classifier,
                             **self.cfg('net', self.default_net))
        self.resize_net()
        self.ut = MoebiusUT()

        self.init_gl()

        self.context.add_handler(pygame.VIDEORESIZE, self.resize_event)

        auto = self.cfg('connect', [])
        with midi.jack.create_client(autoconnect = auto) as client:
            self.client = client
            self.context.run()

        self.cleanup_gl()
