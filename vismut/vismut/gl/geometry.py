

from __future__ import division

from math import sin, pi

from OpenGL import GL

import numpy

from manganese.math.vector import Vec2


def circle(center, radius, subdivisions=3, z=1.5, scale=None):
    translate = Vec2(center)
    r = radius * sin(pi / 4)

    if scale is not None:
        x, y = r * scale[0], r * scale[1]
    else:
        x, y = r, r

    vertices = [[-x, -y, z, 0.0, 0.0],
                [x, -y, z, 1.0, 0.0],
                [-x, y, z, 0.0, 1.0],
                [x, -y, z, 1.0, 0.0],
                [x, y, z, 1.0, 1.0],
                [-x, y, z, 0.0, 1.0],
                ]

    def subdivide(fr, to, subdivisions):
        if subdivisions <= 0:
            return

        base = -fr + to
        new = translate - base.normal.normalized * radius

        if scale is not None:
            new = Vec2(new[0] * scale[0],
                       new[1] * scale[1])

        vertices.extend([[fr[0], fr[1], z, 0.0, 0.0],
                         [new[0], new[1], z, 0.0, 0.0],
                         [to[0], to[1], z, 0.0, 0.0],
                         ])

        subdivide(fr, new, subdivisions - 1)
        subdivide(new, to, subdivisions - 1)

    subdivide(Vec2(-x, -y), Vec2(x, -y), subdivisions)
    subdivide(Vec2(x, -y), Vec2(x, y), subdivisions)
    subdivide(Vec2(x, y), Vec2(-x, y), subdivisions)
    subdivide(Vec2(-x, y), Vec2(-x, -y), subdivisions)

    return vertices
