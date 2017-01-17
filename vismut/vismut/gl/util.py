########################################################################
# manganese - midi analysis & visualization platform
# Copyright (c) 2010, 2011, 2013 Maximilian Marx <mmarx@wh2.tu-dresden.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA.
########################################################################

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
def client_state(state):
    GL.glEnableClientState(state)
    yield
    GL.glDisableClientState(state)


@contextmanager
def vertex_attrib_array(array):
    GL.glEnableVertexAttribArray(array)
    yield
    GL.glDisableVertexAttribArray(array)


@contextmanager
def draw_vbo(array, vbo, stride=0):
    with bind(vbo):
        with vertex_attrib_array(array):
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, stride, vbo)
            yield


@contextmanager
def enabled(property):
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
