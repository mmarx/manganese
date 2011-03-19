

from __future__ import division

from math import sin, pi

from OpenGL import GL

import numpy

from manganese.math.vector import Vec2


def circle(center, radius, subdivisions=3, z=1.5, scale=None):
    translate = Vec2(center)
    r = radius * sin(pi/4)

    if scale:
        x, y = r * scale[0], r * scale[1]
    else:
        x, y = r, r
    
    vertices = [[-x, -y, z],
                [x, -y, z],
                [-x, y, z],
                [x, y, z],
                ]
    
    def subdivide(from, to, subdivisions):
        base = -from + to
        new = translate + base.normal.normalized * radius

        subdivide(from, new, subdivisions - 1)
        subdivide(new, to, subdivisions - 1)

    pass

