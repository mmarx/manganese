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

    def __init__(self, pitchClassifier, anchor=0):
        self.pitchClassifier = pitchClassifier
        self.anchor = anchor
        self.grid = self.pitchClassifier.grid

    def _c(self, tone):
        return self.pitchClassifier.classify(tone)

    def _n(self, pitch, augment=True):
        return self.pitchClassifier.name(pitch, augment)

    def relative_pitch(self, tone):
        return self._c(self._c(tone) - self._c(self.anchor))

    def coordinates(self, pitch):
        return self.coords[pitch]

    def pitch_at(self, x, y):
        return self._c(x * 7 + y * 4 + self.anchor)

    def name(self, x, y, augment=True):
        return self._n(self._c(x * 7 + y * 4), augment)

    def move(self, anchor):
        self.anchor = self._c(anchor)

    def print_net(self, mark=None):
        first = True

        if mark:
            marked = [self._c(x) for x in mark]

        for line in [['_', 9, 4, 11, 6], [10, 5, 0, 7, 2], ['_', 1, 8, 3]]:
            for elt in line:
                if elt == '_':
                    print ' ' * (self.grid + (2 if mark else 0)),
                else:
                    pitch = self.pitch_at(*self.coordinates(elt))
                    name = self._n(pitch, augment=first)
                    pad = (max(1, self.grid + (2 if mark else 0)
                               - len(name)) - 1)

                    if mark:
                        if pitch in marked:
                            print '[%s]' % name,
                            pad -= 2
                        else:
                            print '%s' % name,
                    else:
                        print name,
                    print ' ' * pad,
            print
            first = False
