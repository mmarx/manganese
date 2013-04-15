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

import OpenGL

from OpenGL import GL
from OpenGL.arrays import vbo

from manganese.vismut import gl

import manganese.vismut.gl.util

from . import Theme

class StarsTheme(Theme):
    colors = {'screen_bg': (0, 0, 0, 255),
              'screen_fg': (230, 230, 230, 128),
              'screen_hl': (230, 230, 230, 128),
              'key_bg': {'active': (250, 250, 100, 255),
                         'inactive': (210, 210, 160, 0),
                         'anchor': (255, 255, 120, 255),
                         'anchor_active': (255, 255, 50, 255),
                         'anchor_old': (255, 180, 50, 255),
                         },
              'key_fg': (80, 80, 80, 255),
              'chord_bg': {'major': (255, 255, 0, 255),
                           'minor': (255, 100, 0, 255),
                           },
              }

    def __init__(self, *args, **kwargs):
        super(StarsTheme, self).__init__(*args, **kwargs)

    def node_type(self, x, y):
        is_anchor = self.tn.is_anchor(x, y)

        if self.tn.is_active(x, y):
            if is_anchor:
                return 'anchor_active'
            else:
                return 'active'

        if is_anchor:
            return 'anchor'

        if (x, y) in self.trace:
            return 'anchor_old'

        return 'inactive'

    def draw_trace(self):
        count = len(self.trace)

        if count == 1:
            return

        if count > self.traced_up_to:
            for i in range(self.traced_up_to, count):
                self.add_arrow(src=self.trace[i - 1],
                               dst=self.trace[i],
                               index=i)

            self.traced_up_to = count
            self._geometry('trace', self.trace_vertices)

        GL.glBindTexture(GL.GL_TEXTURE_1D, self.trace_map)
        GL.glUniform1i(self._loc('trace', 'color_map'), 0)
        GL.glUniform1i(self._loc('trace', 'arrows'), count - 1)

        loc = self._loc('trace', 'arrow_id')
        with gl.util.draw_vbo(0, self.vbos['trace'], stride=16):
            with gl.util.vertex_attrib_array(loc):
                GL.glLineWidth(2)
                GL.glVertexAttribPointer(loc, 1, GL.GL_FLOAT, False,
                                         16, self.vbos['trace'] + 12)
                GL.glDrawArrays(GL.GL_LINES, 0, self.vertices['trace'])
                GL.glLineWidth(1)

    def draw_grid(self):
        pass

    def draw_cage(self):
        pass

    def trace_colors(self, steps):
        return gl.textures.trace_colors(steps=steps, last=40)
