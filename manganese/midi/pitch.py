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
    def name(self, pitch, augment=True):
        if pitch in self.base_pitches:
            return self.base_names[self.base_pitches.index(pitch)]
        else:
            if augment:
                index = self.base_pitches.index((pitch - 1) % 12)
                return self.augment(self.base_names[index])
            else:
                index = self.base_pitches.index((pitch + 1) % 12)
                return self.diminish(self.base_names[index])


class NamingDE(Naming):
    base_names = ['c', 'd', 'e', 'f', 'g', 'a', 'h']
    base_pitches = [0, 2, 4, 5, 7, 9, 11]
    grid = 4

    def augment(self, tone):
        if tone == 'b':
            return 'h'

        if tone[-2:] == 'es':
            return tone[:-2]

        return tone + 'is'

    def diminish(self, tone):
        if tone == 'h':
            return 'b'

        if tone in ['a', 'e']:
            return tone + 's'

        if tone[-2:] == 'is':
            return tone[:-2]

        return tone + 'es'


class NamingEN(Naming):
    base_names = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
    base_pitches = [0, 2, 4, 5, 7, 9, 11]
    grid = 7

    def augment(self, tone):
        if tone[-5:] == '-flat':
            return tone[:-5]

        return tone + '-sharp'

    def diminish(self, tone):
        if tone[-6:] == '-sharp':
            return tone[-6:]

        return tone + '-flat'


class PitchClassifier(object):
    def __init__(self, naming=NamingEN):
        self.naming = naming()
        self.grid = self.naming.grid

    def name(self, pitch, augment=True):
        return self.naming.name(pitch, augment)

    def classify(self, pitch):
        return (pitch % 12)
