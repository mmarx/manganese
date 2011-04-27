

from __future__ import division

from math import sqrt
from numbers import Number


class Vec2(object):

    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], Vec2):
                self.vec = args[0].vec
            elif isinstance(args[0], complex):
                self.vec = (args[0].real, args[0].imag)
            elif len(args[0]) == 2:
                self.vec = tuple(args[0])
            else:
                raise TypeError("Can't construct Vec2 from %s."
                                % type(args[0]))
        elif len(args) == 2:
            self.vec = tuple(args)
        else:
            raise TypeError("Wrong number of arguments (%d given)."
                            % len(args))

    def __repr__(self):
        return 'Vec2(%s)' % repr(self.vec)

    def __getitem__(self, index):
        return self.vec[index]

    def __add__(self, other):
        if not isinstance(other, Vec2):
            return NotImplemented

        return Vec2(self[0] + other[0],
                    self[1] + other[1])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vec2([other * elt for elt in self.vec])

        if isinstance(other, Vec2):
            return (self[0] * other[0] +
                    self[1] * other[1])

        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Number):
            return self.__mul__(other)

        return NotImplemented

    def __neg__(self):
        return self * -1

    @property
    def norm(self):
        return sqrt(self * self)

    @property
    def normal(self):
        return Vec2(-self[1], self[0])

    @property
    def normalized(self):
        return self * (1 / self.norm)
