

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

    vertices = [[-x, -y, z],
                [x, -y, z],
                [-x, y, z],
                [x, -y, z],
                [x, y, z],
                [-x, y, z],
                ]

    def subdivide(fr, to, subdivisions):
        if subdivisions <= 0:
            return

        base = -fr + to
        new = translate - base.normal.normalized * radius

        if scale is not None:
            new = Vec2(new[0] * scale[0],
                       new[1] * scale[1])

        vertices.extend([[fr[0], fr[1], z],
                         [new[0], new[1], z],
                         [to[0], to[1], z],
                         ])

        subdivide(fr, new, subdivisions - 1)
        subdivide(new, to, subdivisions - 1)

    subdivide(Vec2(-x, -y), Vec2(x, -y), subdivisions)
    subdivide(Vec2(x, -y), Vec2(x, y), subdivisions)
    subdivide(Vec2(x, y), Vec2(-x, y), subdivisions)
    subdivide(Vec2(-x, y), Vec2(-x, -y), subdivisions)

    return vertices


def label(center, radius, z=1.5, scale=None):
    translate = Vec2(center)
    r = radius * sin(pi / 4)

    if scale is not None:
        x, y = r * scale[0], r * scale[1]
    else:
        x, y = r, r

    return [[-x, -y, z, 0.0, 0.0],
            [x, -y, z, 1.0, 0.0],
            [-x, y, z, 0.0, 1.0],
            [x, y, z, 1.0, 1.0],
            ]


def grid(left, right, bottom, top, z=1.5):
    grid = []

    for column in range(left, right + 1):
        grid.extend([[column, bottom - 1, z],
                     [column, top + 1, z],
                     ])

    for row in range(bottom, top + 1):
        grid.extend([[left - 1, row, z],
                     [right + 1, row, z],
                     ])

    return grid


def cage(offset, scale, z=1.5):
    xo, yo = offset
    xs, ys = scale

    xo *= 2 * xs
    yo *= 2 * ys

    return [[-1 - 0.5 * xo, -1 - yo, z],
            [1 + 0.5 * xo, -1 - yo, z],
            [2 + xo, -0.25 * yo, z],
            [2 + xo, 1 + yo, z],
            [-1 - 0.5 * xo, 1 + yo, z],
            [-2 - 1.125 * xo, 0.0, z],
            [-1 - 0.5 * xo, -1 - yo, z],
            ]
