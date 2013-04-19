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


class Naming(object):
    def _adjust(self, name, amount):
        for _ in range(0, abs(amount)):
            if amount > 0:
                name = self.augment(name)
            else:
                name = self.diminish(name)
        return name

    def name(self, pitch, augment=True, adjust=None):
        if pitch in self.base_pitches:
            name = self.base_names[self.base_pitches.index(pitch)]
            if adjust is not None:
                name = self._adjust(name, adjust)
            return name
        else:
            if augment:
                index = self.base_pitches.index((pitch - 1) % 12)
                name = self.augment(self.base_names[index])
                if adjust is not None:
                    name = self._adjust(name, adjust)
                return name
            else:
                index = self.base_pitches.index((pitch + 1) % 12)
                name = self.diminish(self.base_names[index])
                if adjust is not None:
                    name = self._adjust(name, adjust)
                return name


class NamingDE(Naming):
    base_names = ['c', 'd', 'e', 'f', 'g', 'a', 'h']
    base_pitches = [0, 2, 4, 5, 7, 9, 11]
    grid = 4

    def augment(self, tone):
        if tone == 'b':
            return 'h'

        if tone == 'heses':
            return 'b'

        if tone in ['as', 'es']:
            return tone[1]

        if tone[-2:] in ['es', 'as']:
            return tone[:-2]

        return tone + 'is'

    def diminish(self, tone):
        if tone == 'h':
            return 'b'

        if tone == 'b':
            return 'heses'

        if tone in ['a', 'e']:
            return tone + 's'

        if tone[-2:] == 'is':
            return tone[:-2]

        if tone[:2] == 'as':
            return tone + 'as'

        return tone + 'es'


class NamingEN(Naming):
    base_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    base_pitches = [0, 2, 4, 5, 7, 9, 11]
    grid = 7
    flat = u'\u266d'
    flat = 'b'
    sharp = u'\u266f'
    sharp = '#'

    def augment(self, tone):
        if tone[-1:] == self.flat:
            return tone[:-1]

        return tone + self.sharp

    def diminish(self, tone):
        if tone[-1:] == self.sharp:
            return tone[-1:]

        return tone + self.flat


class PitchClassifier(object):
    def __init__(self, naming=NamingEN):
        self.naming = naming()
        self.grid = self.naming.grid

    def name(self, pitch, augment=True):
        return self.naming.name(pitch, augment)

    def classify(self, pitch):
        return (pitch % 12)
