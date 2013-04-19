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


from manganese.midi import pitch


class ToneNet(object):
    coords = {0: (0, 0),
              1: (-1, -1),
              2: (2, 0),
              3: (1, -1),
              4: (0, 1),
              5: (-1, 0),
              6: (2, 1),
              7: (1, 0),
              8: (0, -1),
              9: (-1, 1),
              10: (-2, 0),
              11: (1, 1),
              }

    def __init__(self, left=-3, right=3,
                 bottom=-2, top=2,
                 anchor=(0, 0),
                 classifier=pitch.NamingDE()):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.anchor = anchor
        self.set_active([])
        self.classifier = classifier

    def _name(self, base, adjust):
        return self.classifier.name(pitch=base * 7 % 12,
                                    augment=(adjust >= 0),
                                    adjust=adjust)

    def name(self, x, y):
        base = x + 4 * y
        adjust = 0

        while base < -1:
            adjust -= 1
            base += 7

        while base > 5:
            adjust += 1
            base -= 7

        return self._name(base, adjust)

    @property
    def columns(self):
        return self.right - self.left + 1

    @property
    def rows(self):
        return self.top - self.bottom + 1

    def rebase(self, anchor):
        self.anchor = anchor

    def move(self, anchor_pitch):
        self.rebase(self.pitch_coordinates(anchor_pitch))

    def is_fundamental(self, x, y):
        clip = {1: (-1, 2),
                0: (-2, 2),
                -1: (-1, 1),
                }

        ax, ay = self.anchor

        if abs(y - ay) > 1:
            return False

        l, r = clip[y - ay]

        if l <= (x - ax) <= r:
            return True
        return False

    def is_anchor(self, x, y):
        return (x, y) == self.anchor

    def pitch_coordinates(self, pitch, relative=False):
        ax, ay = self.anchor
        anchor_pitch = ax * 7 + ay * 4
        pitch_class = (pitch - anchor_pitch) % 12
        rx, ry = self.coords[pitch_class]

        if relative:
            ax = ay = 0

        return (ax + rx, ay + ry)

    def set_active(self, keys):
        self.active = [self.pitch_coordinates(key) for key in keys]

    def is_active(self, x, y):
        return (x, y) in self.active

    def should_grow(self, min_dist=0):
        ax, ay = self.anchor

        return min(ax - 2 - self.left,
                   self.right - ax - 2,
                   self.top - ay - 1,
                   ay - 1 - self.bottom) < min_dist

    def grow(self, min_dist=0, by=2):
        ax, ay = self.anchor

        dist = ax - 2 - self.left
        if dist < min_dist:
            self.left -= max(by, min_dist - dist)

        dist = self.right - ax - 2
        if dist < min_dist:
            self.right += max(by, min_dist - dist)

        dist = self.top - ay - 1
        if dist < min_dist:
            self.top += max(by, min_dist - dist)

        dist = ay - 1 - self.bottom
        if dist < min_dist:
            self.bottom -= max(by, min_dist - dist)
