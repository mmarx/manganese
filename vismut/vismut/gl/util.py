

from __future__ import division

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
def enable(property):
    GL.glEnable(property)
    yield
    GL.glDisable(property)


def transformation_matrix(program, matrix):
    location = GL.glGetUniformLocation(program, "transformation")
    GL.glUniformMatrix4fv(location, 1, True, matrix)


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
