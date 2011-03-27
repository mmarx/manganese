

from __future__ import division

from math import sin, pi

from OpenGL import GL

import numpy

from manganese.math.vector import Vec2


def circle(radius, subdivisions=3, z=1.5, scale=None):
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
        new = -base.normal.normalized * radius

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


def label(radius, z=0.5, scale=None):
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


def grid(left, right, bottom, top, z=0.5):
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


def cage(offset, scale, z=0.5):
    xo, yo = offset
    xs, ys = scale

    xo *= xs
    yo *= ys

    return [[-1 - 0.5 * xo, -1 - yo, z],
            [1 + 0.5 * xo, -1 - yo, z],
            [2 + xo, -0.25 * yo, z],
            [2 + xo, 1 + yo, z],
            [-1 - 0.5 * xo, 1 + yo, z],
            [-2 - 1.125 * xo, 0.0, z],
            [-1 - 0.5 * xo, -1 - yo, z],
            ]


def chords(major, minor, z=0.45):
    return [[0.0, 0.0, z] + major,      # 0
            [1.0, 0.0, z] + major,      # 1
            [0.0, 1.0, z] + major,      # 2
            [1.0, 1.0, z] + major,      # 3
            [2.0, 0.0, z] + major,      # 4
            [-1.0, 1.0, z] + major,     # 5
            [-1.0, 0.0, z] + major,     # 6
            [-1.0, -1.0, z] + major,    # 7
            [0.0, -1.0, z] + major,     # 8
            [1.0, -1.0, z] + major,     # 9
            [0.0, 0.0, z] + minor,      # 10
            [0.0, 1.0, z] + minor,      # 11
            [-1.0, 1.0, z] + minor,     # 12
            [-1.0, 0.0, z] + minor,     # 13
            [-1.0, -1.0, z] + minor,    # 14
            [-2.0, 0.0, z] + minor,     # 15
            [1.0, 0.0, z] + minor,      # 16
            [1.0, 1.0, z] + minor,      # 17
            [1.0, -1.0, z] + minor,     # 18
            [2.0, 0.0, z] + minor,      # 19
            [2.0, 1.0, z] + minor,      # 20
            [0.0, -1.0, z] + minor,     # 21
            ]
