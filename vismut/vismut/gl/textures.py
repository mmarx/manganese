
from __future__ import division

from math import ceil, log

from OpenGL import GL

import pygame
import pygame.image


def node_label(label):
    size = 2 ** ceil(log(max(label.get_size()), 2))
    surface = pygame.surface.Surface((size, size),
                                     flags=pygame.SRCALPHA).convert_alpha()
    surface.fill((0, 0, 0, 0))
    surface.blit(label, label.get_rect(center=(size // 2, size // 2)))

    data = pygame.image.tostring(surface, "RGBA", True)

    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_2D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S,
                       GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T,
                       GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                       GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                       GL.GL_LINEAR)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, size, size,
                    0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)

    return tex


def trace_colors(steps):
    def rgb_from_hsv(h, s, v, a=None):
        hi = h // 60
        f = (h / 60) - hi
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if hi in [0, 6]:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        else:
            raise ValueError("h_i out of range")

        if a is None:
            return (r, g, b)
        else:
            return (r, g, b, a)

    def color(index, alpha=None):
        return tuple([min(max(0, int(component * 255)), 255)
                      for component
                      in rgb_from_hsv((index % 361),
                                      0.75 + index / (4 * steps),
                                      0.75 + index / (4 * steps),
                                      alpha)])

    surface = pygame.surface.Surface((steps, 1),
                                     flags=pygame.SRCALPHA).convert_alpha()

    for x in range(0, steps):
        surface.set_at((x, 0), color(x * (360 / steps), alpha=1.0))

    data = pygame.image.tostring(surface, "RGBA", True)

    tex = GL.glGenTextures(1)
    GL.glActiveTexture(GL.GL_TEXTURE0)
    GL.glBindTexture(GL.GL_TEXTURE_1D, tex)
    GL.glTexParameteri(GL.GL_TEXTURE_1D, GL.GL_TEXTURE_WRAP_S,
                       GL.GL_REPEAT)
    GL.glTexParameteri(GL.GL_TEXTURE_1D, GL.GL_TEXTURE_MAG_FILTER,
                       GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_1D, GL.GL_TEXTURE_MIN_FILTER,
                       GL.GL_LINEAR)
    GL.glTexImage1D(GL.GL_TEXTURE_1D, 0, GL.GL_RGBA, steps,
                    0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)

    return tex
