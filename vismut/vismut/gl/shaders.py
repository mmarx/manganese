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
