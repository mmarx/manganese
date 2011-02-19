
from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER

VERTEX, FRAGMENT = range(2)

_extensions = {VERTEX: 'vert',
               FRAGMENT: 'frag',
               }

_types = {VERTEX: GL_VERTEX_SHADER,
          FRAGMENT: GL_FRAGMENT_SHADER,
          }


def filename(basename, type):
    return '%s.%s' % (basename, _extensions[type])


def compile_shader(shader, type):
    """Compile a shader"""
    return shaders.compileShader(shader, _types[type])
