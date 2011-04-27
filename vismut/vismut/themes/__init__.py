
import OpenGL
import numpy

from OpenGL import GL
from OpenGL.arrays import vbo

from manganese.vismut import gl

import manganese.vismut.gl.util
import manganese.vismut.gl.textures

import manganese.math.vector as vector


class ThemeLoadingError(Exception):
    pass


_themes = {}


def get(name, app):
    if name in _themes:
        return _themes[name]
        
    theme = None
    try:
        theme = __import__(name, globals=globals())
    except ImportError:
        raise ThemeLoadingError("No such theme: `%s'" % name)
    except Exception, e:
        raise ThemeLoadingError("Failed to load theme:"
                                " `%s': %s" % (name, e))

    clsname = '%sTheme' % name.title()
    try:
        the_theme = getattr(theme, clsname)

        if not issubclass(the_theme, Theme):
            raise ThemeLoadingError("Incomplete theme definition: "
                                    "`%s'" % name)
        
        _themes[name] = the_theme(app=app)
        return _themes[name]
    except AttributeError:
        raise ThemeLoadingError("Theme file does not define a theme: "
                                "`%s'" % name)


class Theme(object):
    def __init__(self, app):
        self.app = app

    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]

        if hasattr(self.app, attr):
            return getattr(self.app, attr)

        return NotImplemented
        
    @gl.util.normalized_color
    def color(self, name, type, subtype=None):
        qualified_name = '%s_%s' % (name, type)

        if qualified_name in self.colors:
            color = self.colors[qualified_name]

            if isinstance(color, dict):
                if subtype is not None:
                    return color[subtype]
            else:
                return color

    def node_type(self, x, y):
        is_anchor = self.tn.is_anchor(x, y)

        if self.tn.is_active(x, y):
            if (x, y) == (0, 0):
                return 'anchor_initial_active'

            if is_anchor:
                return 'anchor_active'
            else:
                return 'active'
        elif (x, y) == (0, 0):
            return 'anchor_initial'

        if is_anchor:
            return 'anchor'

        return 'inactive'

    def draw(self):
        self.tn.set_active(self.ut.keys)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        x, y = self.tn.anchor

        with gl.util.use_program(self.programs['flat']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('flat',
                                                             'transformation'))

            with gl.util.draw_vbo(0, self.vbos['node']):
                for column in range(self.tn.left, self.tn.right + 1):
                    for row in range(self.tn.bottom, self.tn.top + 1):
                        self.draw_node(column, row)

            GL.glUniform3f(self._loc('flat', 'translation'), 0.0, 0.0, 0.0)
            self.draw_grid()

        with gl.util.use_program(self.programs['flat-attrib']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('flat-attrib',
                                                             'transformation'))
            GL.glUniform3f(self._loc('flat-attrib', 'translation'), x, y, 0.0)

            self.draw_cage()
            self.draw_chords([self.tn.pitch_coordinates(key, relative=True)
                              for key in self.ut.keys])

        with gl.util.use_program(self.programs['trace']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('trace',
                                                             'transformation'))
            self.draw_trace()

        with gl.util.use_program(self.programs['textured']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('textured',
                                                             'transformation'))
            with gl.util.draw_vbo(0, self.vbos['label'], stride=20):
                GL.glUniform1i(self._loc('textured', 'texture'), 0)
                loc = self._loc('textured', 'tex_coords')
                with gl.util.vertex_attrib_array(loc):
                    GL.glVertexAttribPointer(loc, 2, GL.GL_FLOAT, False,
                                             20, self.vbos['label'] + 12)
                    for column in range(self.tn.left, self.tn.right + 1):
                        for row in range(self.tn.bottom, self.tn.top + 1):
                            self.draw_node_label(column, row)

    def draw_node(self, column, row):
        GL.glUniform3f(self._loc('flat', 'translation'), column, row, 0)
        GL.glUniform4f(self._loc('flat', 'color'),
                       *self.color('key', 'bg',
                                         self.node_type(column, row)))
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.vertices['node'])

    def draw_node_label(self, column, row):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.textures[column][row])
        GL.glUniform3f(self._loc('textured', 'translation'), column, row, 0)
        GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 0, self.vertices['label'])

    def draw_chords(self, nodes):
        if len(nodes) < 3:
            return

        indices = []

        if (0, 0) in nodes:
            if (0, 1) in nodes:
                if (1, 0) in nodes:
                    indices.extend([0, 1, 2])
                if (-1, 1) in nodes:
                    indices.extend([10, 11, 12])

            if (0, -1) in nodes:
                if (1, -1) in nodes:
                    indices.extend([0, 8, 9])
                if (-1, 0) in nodes:
                    indices.extend([10, 21, 13])

            if (-1, 0) in nodes and (-1, 1) in nodes:
                indices.extend([0, 6, 5])

            if (1, 0) in nodes and (1, -1) in nodes:
                indices.extend([10, 16, 18])

        if (-1, 0) in nodes and (-1, -1) in nodes:
            if (-2, 0) in nodes:
                indices.extend([13, 14, 15])
            if (0, -1) in nodes:
                indices.extend([6, 7, 8])

        if (1, 1) in nodes:
            if (2, 0) in nodes and (2, 1) in nodes:
                indices.extend([17, 19, 20])
            if (1, 0) in nodes:
                if (2, 0) in nodes:
                    indices.extend([3, 1, 4])
                if (0, 1) in nodes:
                    indices.extend([17, 16, 11])

        if not indices:
            return

        outline = []
        for i in range(0, len(indices), 3):
            outline.extend([indices[i] + 22,
                            indices[i + 1] + 22,
                            indices[i + 1] + 22,
                            indices[i + 2] + 22,
                            indices[i + 2] + 22,
                            indices[i] + 22])

        loc = self._loc('flat-attrib', 'color')
        bg = vbo.VBO(numpy.array(indices, 'uint8'),
                      target='GL_ELEMENT_ARRAY_BUFFER')
        ol = vbo.VBO(numpy.array(outline, 'uint8'),
                     target='GL_ELEMENT_ARRAY_BUFFER')

        with gl.util.draw_vbo(0, self.vbos['chords'], stride=28):
            with gl.util.vertex_attrib_array(loc):
                GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False,
                                         28, self.vbos['chords'] + 12)
                with gl.util.bind(bg):
                    GL.glDrawElements(GL.GL_TRIANGLES, len(indices),
                                      GL.GL_UNSIGNED_BYTE, bg)
                with gl.util.bind(ol):
                    GL.glDrawElements(GL.GL_LINES, len(outline),
                                      GL.GL_UNSIGNED_BYTE, bg)

    def add_arrow(self, src, dst, index, z=0.625):
        def point(p):
            return [p[0], p[1], z, index]

        s = vector.Vec2(src)
        d = vector.Vec2(dst)

        is_unit = (d - s).norm == 1

        if is_unit:
            is_arc = False
        else:
            is_arc = (s[0] == d[0]) or (s[1] == d[1])

        points = [point(src),
                  point(dst),
                  ]

        offset = self.node_radius * 0.175 * 2
        direction = (-s + d).normalized

        points[0][0:2] = (s + direction * self.node_radius +
                          direction.normal * offset).vec
        points[1][0:2] = (d - direction * self.node_radius +
                          direction.normal * offset).vec
        mid = (vector.Vec2(points[1][0:2]) -
               (direction * offset))

        if is_arc:
            points.insert(1, point(vector.Vec2(points[1][0:2]) -
                                   direction * offset +
                                   direction.normal * offset))
            points.insert(1, points[1])
            points.insert(1, point(vector.Vec2(points[0][0:2]) +
                                   direction * offset +
                                   direction.normal * offset))
            points.insert(1, points[1])

        points.append(points[-1])
        points.append(point((mid + direction.normal * offset)))
        points.append(points[-1])
        points.append(point((mid - direction.normal * offset)))
        points.append(points[-1])
        points.append(points[5 if is_arc else 1])

        self.trace_vertices = numpy.append(self.trace_vertices,
                                           numpy.array(points, 'f'),
                                           axis=0)

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
                GL.glLineWidth(4)
                GL.glVertexAttribPointer(loc, 1, GL.GL_FLOAT, False,
                                         16, self.vbos['trace'] + 12)
                GL.glDrawArrays(GL.GL_LINES, 0, self.vertices['trace'])
                GL.glLineWidth(1)

    def draw_grid(self):
        with gl.util.draw_vbo(0, self.vbos['grid']):
            GL.glUniform4f(self._loc('flat', 'color'),
                           *self.color('key', 'bg', 'inactive'))
            GL.glDrawArrays(GL.GL_LINES, 0, self.vertices['grid'])

    def draw_cage(self):
        loc = self._loc('flat-attrib', 'color')

        with gl.util.draw_vbo(0, self.vbos['cage'], stride=28):
            with gl.util.vertex_attrib_array(loc):
                GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False,
                                         28, self.vbos['cage'] + 12)
                GL.glDrawArrays(GL.GL_LINE_STRIP, 0, 7)
                GL.glDrawArrays(GL.GL_TRIANGLE_STRIP, 7, 6)

    def trace_colors(self, steps):
        return gl.textures.trace_colors(steps=steps, last=360)


