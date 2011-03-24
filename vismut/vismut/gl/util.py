

from __future__ import division

from functools import wraps

from OpenGL import GL

import numpy

from contextlib import contextmanager


@contextmanager
def use_program(program):
    GL.glUseProgram(program)
    yield program
    GL.glUseProgram(0)


@contextmanager
def bind(buffer):
    buffer.bind()
    yield
    buffer.unbind()


@contextmanager
def enable_client_state(state):
    GL.glEnableClientState(state)
    yield
    GL.glDisableClientState(state)


@contextmanager
def draw_vbo(array, vbo, stride=0):
    with bind(vbo):
        GL.glEnableVertexAttribArray(array)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, stride, vbo)
        yield
        GL.glDisableVertexAttribArray(array)


@contextmanager
def enable(property):
    GL.glEnable(property)
    yield
    GL.glDisable(property)


def transformation_matrix(program, matrix, location=None):
    if location is None:
        loc = GL.glGetUniformLocation(program, "transformation")
    else:
        loc = location

    GL.glUniformMatrix4fv(loc, 1, True, matrix)


def ortho(left, right, bottom, top, near, far):
    rl = left - right
    tb = bottom - top
    fn = far - near

    return numpy.matrix([
        [-2 / rl, 0, 0, (right + left) / rl],
        [0, -2 / tb, 0, (top + bottom) / tb],
        [0, 0, -2 / fn, (far + near) / fn],
        [0, 0, 0, 1],
        ], 'f')


def normalized_color(f, default_alpha=1.0):
    @wraps(f)
    def wrapper(*args, **kwargs):
        color = f(*args, **kwargs)
        norm = [component / 255 for component in color]

        if len(color) == 3:
            norm.append(default_alpha)

        return tuple(norm)

    return wrapper
