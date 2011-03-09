

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

    def __init__(self, left=-3, right=7, bottom=-2, top=2, anchor=(0, 0)):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.anchor = anchor
        self.set_active([])

    def _name(self, base, adjust):
        default_policy = lambda c: abs(c) * ('es' if (c < 0) else 'is')
        basenames = {-1: 'f',
                     0: 'c',
                     1: 'g',
                     2: 'd',
                     3: 'a',
                     4: 'e',
                     5: 'h',
                     }

        policies = {3: (lambda c: (abs(c) * 'as' if (c < 0)
                                  else 'a' + c * 'is')),
                    4: (lambda c: (abs(c) * 'es' if (c < 0)
                                  else 'e' + c * 'is')),
                    5: (lambda c: ('b' if (c == -1)
                                  else 'h' + default_policy(c))),
                    }

        if base in policies:
            return policies[base](adjust)
        else:
            return basenames[base] + default_policy(adjust)

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

    def pitch_coordinates(self, pitch):
        ax, ay = self.anchor
        anchor_pitch = ax * 7 + ay * 4
        pitch_class = (pitch - anchor_pitch) % 12
        rx, ry = self.coords[pitch_class]

        return (ax + rx, ay + ry)

    def set_active(self, keys):
        self.active = [self.pitch_coordinates(key) for key in keys]

    def is_active(self, x, y):
        return (x, y) in self.active

    def should_grow(self, min_dist=0):
        ax, ay = self.anchor

        if min(ax - 2 - self.left,
               self.right - ax - 2,
               self.top - ay - 1,
               ay - 1 - self.bottom) < min_dist:
            return True
        return False

    def grow(self, min_dist=0, by=2):
        ax, ay = self.anchor

        if (ax - 2 - self.left) < min_dist:
            self.left -= by
        if (self.right - ax - 2) < min_dist:
            self.right += by
        if (self.top - ay - 1) < min_dist:
            self.top += by
        if (ay - 1 - self.bottom) < min_dist:
            self.bottom -= by
