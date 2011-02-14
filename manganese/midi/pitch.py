

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
