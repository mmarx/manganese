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

from math import ceil

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
    def __init__(self, grow=True, *args, **kwargs):
        self.do_grow = grow
        super(MoebiusNet, self).__init__(*args, **kwargs)

    coords = {0: (0, 0),        # C
              2: (2, 4),        # D
              4: (4, 1),        # E
              5: (6, 5),        # F
              7: (1, 2),        # G
              9: (3, 6),        # A
              11: (5, 3),       # B
          }
    offset = 0

    def clamp(self, x, y):
        w = self.left - self.right


        if x < self.left or x > self.right:
            x = ((ceil(abs(w / 7.0)) * 7) % abs(w)) + (x % w)

        return x, y

    def name(self, x, y):
        base = x + 4 * y

        while base < -1:
            base += 7

        while base > 5:
            base -= 7

        return self._name(base, 0)

    def should_grow(self, *args, **kwargs):
        if not self.do_grow:
            return
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
        lx = ax -1
        if not self.do_grow and lx < self.left:
            lx = self.right

        coordinates = [(lx, (dy - (2 * (ox - 1))) % 7),
                       (ax, (dy - (2 * ox)) % 7),
        ]

        return coordinates

    def move(self, pitch):
        ax, ay = self.anchor
        dx, dy = self.coords[pitch % 12]

        if ax % 7 == 0:
            if dx < ax:
                self.offset = ax + 7
            elif dx > ax:
                self.offset = ax - 7

        self.anchor = (self.offset + dx % 7, ay)

        if not self.do_grow:
            self.anchor = self.clamp(*self.anchor)

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
        self.mode = mode
        self.context.setup(mode)
        self.aspect = mode[0] / mode[1]

        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)
        self.font_atlas = gl.textures.font_atlas(self.data('vera.ttf'),
                                                 0, 128)
        theme = themes.get(self.cfg('theme', 'default'), self)

        class Theme(theme.__class__):
            chords = [{'major': [2, 22, 32,
                                 22, 32, 33,
                             ],
                       'minor': [11, 27, 38,
                                 27, 38, 39,
                             ],
                       'dim': [44, 45, 52,
                               45, 52, 53,
                           ],
                   },
                      {'major': [22, 23, 33,
                                 23, 33, 34,
                             ],
                       'minor': [27, 28, 39,
                                 28, 39, 40,
                             ],
                       'dim': [45, 46, 53,
                               46, 53, 54,
                           ],
                   },
                      {'major': [23, 24, 34,
                                 24, 34, 35,
                             ],
                       'minor': [28, 29, 40,
                                 29, 40, 41,
                             ],
                       'dim': [46, 47, 54,
                               47, 54, 55,
                           ]
                   },
                      {'major': [24, 25, 35,
                                 25, 35, 36,
                             ],
                       'minor': [29, 30, 41,
                                 30, 41, 42,
                             ],
                       'dim': [47, 48, 55,
                               48, 55, 56,
                           ],
                   },
                      {'major': [25, 26, 36,
                                 2, 5, 32,
                                 0, 2, 5,
                                 10, 12, 13,
                                 10, 13, 63,
                                 6, 58, 59,
                                 31, 61, 64,
                                 26, 36, 57,
                             ],
                       'major-minor': [25, 26, 36,
                                       11, 37, 38,
                                       10, 11, 12,
                                       43, 50, 51,
                                       43, 50, 67,
                                       49, 66, 68,
                                       6, 58, 59,
                                       26, 36, 57,
                                   ],
                       'minor': [30, 31, 42,
                                 11, 37, 38,
                                 10, 11, 12,
                                 0, 5, 6,
                                 0, 6, 59,
                                 26, 57, 60,
                                 13, 62, 63,
                                 31, 42, 61,
                             ],
                       'minor-dim': [30, 31, 42,
                                     44, 51, 52,
                                     43, 44, 51,
                                     0, 5, 6,
                                     0, 6, 59,
                                     13, 62, 63,
                                     31, 42, 61,
                                     26, 57, 60,
                                 ],
                       'dim-major': [48, 49, 56,
                                     2, 5, 32,
                                     0, 2, 5,
                                     10, 12, 13,
                                     10, 13, 63,
                                     50, 65, 67,
                                     49, 56, 66,
                                     31, 61, 64,
                                 ],
                   },
                  ]

            chord_types = {0: ['major', 'minor', 'major', 'dim', 'minor'],
                           1: ['major', 'dim', 'minor', 'major', 'minor'],
                           2: ['minor', 'major', 'minor', 'major', 'minor-dim'],
                           3: ['minor', 'major', 'minor', 'major', 'dim-major'],
                           4: ['minor', 'major', 'dim', 'minor', 'major'],
                           5: ['dim', 'minor', 'major', 'minor', 'major'],
                           6: ['major', 'minor', 'major', 'minor', 'major-minor'],
                           }

            def draw_cage(self):
                pass

            def _chord(self, idx):
                type = self.chord_types[self.tn.anchor[0] % 7][idx]
                return self.chords[idx][type]

            def draw_chords(self, keys):
                if len(keys) < 3:
                    return

                nodes = []
                for idx in range(0, len(keys[0])):
                    nodes.extend([key[idx] for key in keys])

                indices = []

                if (0, 0) in nodes:
                    if (0, 1) in nodes:
                        if (-1, 2) in nodes:
                            indices.extend(self._chord(0))
                            if (0, 3) in nodes:
                                indices.extend(self._chord(1))
                                if (0, 4) in nodes:
                                    indices.extend(self._chord(2))
                                    if (0, 5) in nodes:
                                        indices.extend(self._chord(3))
                                        if (0, 6) in nodes:
                                            indices.extend(self._chord(4))

                self._draw_chords(indices)

        self.theme = Theme(app=self)
        self.classifier = getattr(manganese.midi.pitch,
                                  'Naming' + self.cfg('naming', 'DE'))()
        self.tn = MoebiusNet(classifier=self.classifier,
                             grow=self.cfg('grow', True),
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
