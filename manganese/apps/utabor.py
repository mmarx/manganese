
from __future__ import division

import sys
import os.path

from math import ceil, log

import numpy
import pygame

import OpenGL

OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True
OpenGL.FULL_LOGGING = False
OpenGL.ERROR_ON_COPY = True
OpenGL.FORWARD_COMPATIBLE_ONLY = True

from OpenGL import GL
from OpenGL.arrays import vbo

import _apps

from manganese.vismut import gl

import manganese.vismut.gl.util
import manganese.vismut.gl.context
import manganese.vismut.gl.shaders
import manganese.vismut.gl.geometry

import manganese.utabor._utabor as utabor
import manganese.midi.jack as jack
import manganese.utabor.centered_net as net
import manganese.math.vector as vector


class Application(_apps.Application):

    default_colors = {'screen_bg': (255, 255, 255, 255),
                      'screen_fg': (0, 0, 0, 255),
                      'screen_hl': (50, 230, 230, 255),
                      'key_bg': {'active': (200, 230, 250, 255),
                                 'inactive': (160, 160, 220, 255),
                                 'anchor': (250, 200, 250, 255),
                                 'anchor_active': (220, 220, 250, 255),
                                 'anchor_initial': (200, 0, 0, 255),
                                 'anchor_initial_active': (255, 0, 0, 255),
                                 },
                      'key_fg': (80, 80, 80, 255),
                      'chord_bg': {'major': (255, 255, 0, 255),
                                   'minor': (255, 200, 0, 255),
                                   },
                      }

    vsync = not True
    max_fps = 0
    anchor = 60
    grow_count = 0
    node_radius = 0.25
    trace = [(0, 0),
             ]

    locs = {}
    vbos = {}
    programs = {}
    textures = {}
    vertices = {}

    def _loc(self, prog, name):
        return self.locs[prog][name]

    @gl.util.normalized_color
    def _color(self, name, type, subtype=None):
        qualified_name = '%s_%s' % (name, type)

        if qualified_name in self.colors:
            color = self.colors[qualified_name]

            if isinstance(color, dict):
                if subtype is not None:
                    return color[subtype]
            else:
                return color

    def _text(self, the_text, color):
        if not self.font:
            return

        return self.font.render(the_text, True, color)

    def _node_type(self, x, y):
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

    def _geometry(self, name, vertices):
        self.vbos[name] = vbo.VBO(numpy.array(vertices, 'f'))
        self.vertices[name] = len(vertices)

    def _program(self, name, program):
        def compile_shader(type):
            with open(self.data(gl.shaders.filename(name, type),
                                app='vismut')) as shader:
                return gl.shaders.compile_shader(shader.read(), type)

        def locs(type, lookup):
            if type in program:
                for loc in program[type]:
                    self.locs[name][loc] = lookup(self.programs[name], loc)

        vertex = compile_shader(gl.shaders.VERTEX)
        fragment = compile_shader(gl.shaders.FRAGMENT)

        self.locs[name] = {}
        self.programs[name] = GL.shaders.compileProgram(vertex, fragment)

        locs('uniforms', GL.glGetUniformLocation)
        locs('attributes', GL.glGetAttribLocation)

    def _make_label(self, column, row):
        label = self._text(self.tn.name(column, row),
                           (0, 0, 0, 255)).convert_alpha()

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

    def draw_node(self, column, row):
        GL.glUniform3f(self._loc('flat', 'translation'), column, row, 0)
        GL.glUniform4f(self._loc('flat', 'color'),
                       *self._color('key', 'bg',
                                    self._node_type(column, row)))
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

        loc = self._loc('flat-attrib', 'color')
        ibo = vbo.VBO(numpy.array(indices, 'uint8'),
                      target='GL_ELEMENT_ARRAY_BUFFER')

        with gl.util.draw_vbo(0, self.vbos['chords'], stride=28):
            with gl.util.vertex_attrib_array(loc):
                GL.glVertexAttribPointer(loc, 4, GL.GL_FLOAT, False,
                                         28, self.vbos['chords'] + 12)
                with gl.util.bind(ibo):
                    GL.glDrawElements(GL.GL_TRIANGLES, len(indices),
                                      GL.GL_UNSIGNED_BYTE, ibo)

    def draw_arrow(self, src, dst, color, z=0.625):
        def point(p):
            return [p[0], p[1], z]

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
            points.insert(1, point(vector.Vec2(points[0][0:2]) +
                                   direction * offset +
                                   direction.normal * offset))

        points.append(point((mid + direction.normal * offset)))
        points.append(point((mid - direction.normal * offset)))
        points.append(points[3 if is_arc else 1])

        v = vbo.VBO(numpy.array(points, 'f'))
        with gl.util.draw_vbo(0, v):
            GL.glUniform4f(self._loc('flat', 'color'), *color)
            GL.glDrawArrays(GL.GL_LINE_STRIP, 0, len(points))

    def draw_trace(self):
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

        def color(index, steps, alpha=None):
            return rgb_from_hsv((steps - i % 361),
                                0.75 + index / (4 * steps),
                                0.75 + index / (4 * steps),
                                alpha)

        count = len(self.trace)

        for i in range(1, count):
            self.draw_arrow(src=self.trace[i - 1],
                            dst=self.trace[i],
                            color=color(i, count - 1, alpha=1.0))

    def draw_grid(self):
        with gl.util.draw_vbo(0, self.vbos['grid']):
            GL.glUniform4f(self._loc('flat', 'color'),
                           *self._color('key', 'bg', 'inactive'))
            GL.glDrawArrays(GL.GL_LINES, 0, self.vertices['grid'])

    def draw_cage(self):
        with gl.util.draw_vbo(0, self.vbos['cage']):
            GL.glUniform4f(self._loc('flat', 'color'),
                           *self._color('screen', 'fg'))
            GL.glDrawArrays(GL.GL_LINE_STRIP, 0, self.vertices['cage'])

    def init_gl(self):
        self.programs = {}
        programs = {'flat': {'uniforms': ['color',
                                          'translation',
                                          'transformation',
                                          ],
                             },
                    'trace': {'uniforms': ['arrows',
                                           'transformation',
                                           'color_map',
                                           ],
                              'attributes': ['arrow_id',
                                             ],
                              },
                    'textured': {'uniforms': ['texture',
                                              'translation',
                                              'transformation',
                                              ],
                                 'attributes': ['tex_coords',
                                                ],
                                 },
                    'flat-attrib': {'uniforms': ['translation',
                                                 'transformation',
                                                 ],
                                    'attributes': ['color',
                                                   ],
                                    },
                    }

        for program in programs:
            self._program(program, programs[program])

        GL.glClearColor(*self._color('screen', 'bg'))
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def cleanup_gl(self):
        GL.glDeleteTextures(numpy.array([self.textures[column][row]
                                         for column in self.textures
                                         for row in self.textures[column]],
                                        'uint32'))
        self.textures = {}

    def resize_event(self, event):
        self.aspect = event.w / event.h
        self.resize_net()

    def resize_net(self):
        self.matrix = gl.util.ortho(self.tn.left - 0.5,
                                    self.tn.right + 0.5,
                                    self.tn.bottom - 0.5,
                                    self.tn.top + 0.5,
                                    0,
                                    1)

        scale = self.tn.columns / self.tn.rows

        if self.aspect <= 1:
            w, h = (self.aspect, 1.0)
        else:
            w, h = (1.0, self.aspect)

        if scale <= 1:
            w /= scale
        else:
            h /= scale

        self.node_size = (w, h)

        self._geometry('node', gl.geometry.circle(radius=self.node_radius,
                                                  scale=self.node_size,
                                                  subdivisions=5,
                                                  z=0.5))

        self._geometry('label', gl.geometry.label(radius=self.node_radius,
                                                  scale=self.node_size,
                                                  z=0.75))

        self._geometry('cage', gl.geometry.cage(offset=(0.5, 0.45),
                                                scale=self.node_size, z=0.25))

        self._geometry('grid', gl.geometry.grid(self.tn.left, self.tn.right,
                                                self.tn.bottom, self.tn.top,
                                                z=0.125))

        self._geometry('chords',
                       gl.geometry.chords(z=0.45,
                                          major=list(self._color('chord', 'bg',
                                                            'major')),
                                          minor=list(self._color('chord', 'bg',
                                                            'minor'))))

        self.polys = (self.tn.columns * self.tn.rows *
                      (self.vertices['node'] + self.vertices['label']) +
                      self.vertices['cage'])

        for column in range(self.tn.left, self.tn.right + 1):
            for row in range(self.tn.bottom, self.tn.top + 1):
                tex = self._make_label(column, row)
                if column in self.textures:
                    if row not in self.textures[column]:
                        self.textures[column][row] = self._make_label(column,
                                                                      row)
                else:
                    self.textures[column] = {row: self._make_label(column,
                                                                   row),
                                             }

    def render(self):
        print '-!- fps:', self.context.clock.get_fps(), 'polys: ', self.polys

        eventful = False

        while self.client.have_events:
            event = self.client.next_event()

            if len(event.raw) <= 4:
                self.ut.handle_midi(event.as_dword())

                if self.ut.anchor_changed:
                    anchor = self.ut.anchor
                    if anchor != self.anchor:
                        self.tn.move(anchor)
                        self.anchor = anchor
                        if self.trace[-1] != self.tn.anchor:
                            self.trace.append(self.tn.anchor)

                if self.tn.should_grow(min_dist=1):
                    self.grow_count += 1

                    if self.grow_count >= self.max_fps // 10:
                        self.tn.grow(min_dist=1, by=1)
                        self.resize_net()
                        self.grow_count = 0

        self.draw()

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
            self.draw_trace()

            GL.glUniform3f(self._loc('flat', 'translation'), x, y, 0.0)

            self.draw_cage()

        with gl.util.use_program(self.programs['flat-attrib']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('flat-attrib',
                                                             'transformation'))
            GL.glUniform3f(self._loc('flat-attrib', 'translation'), x, y, 0.0)

            self.draw_chords([self.tn.pitch_coordinates(key, relative=True)
                              for key in self.ut.keys])

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

    def run(self):
        self.tn = net.ToneNet()

        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps,
                                                vsync=self.vsync)

        mode = self.cfg('mode', '640x480')
        self.context.setup(mode)
        self.aspect = mode[0] / mode[1]

        self.colors = self.cfg('colors', self.default_colors)
        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)

        self.resize_net()

        self.ut = utabor.get_uTabor()
        logic = os.path.join(self.prefix(), 'data', 'utabor', 'demo.mut')
        self.ut.load_logic(logic)
        self.ut.select_action('N', True)

        self.init_gl()

        self.context.add_handler(pygame.VIDEORESIZE, self.resize_event)

        with jack.create_client() as jack_client:
            self.client = jack_client

            self.context.run()

        self.cleanup_gl()

        utabor.destroy_uTabor()
        sys.exit()
