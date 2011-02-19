
from OpenGL import GL

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


def transformation_matrix(program, matrix):
    location = GL.glGetUniformLocation(program, "transformation")
    GL.glUniformMatrix4fv(location, 1, True, matrix)
