
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
    node_radius = 0.75
    trace = [(0, 0),
             ]

    vbos = {}
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

    def draw_chord(self, nodes, type):
        ax, ay = self.tn.anchor
        points = [(ax + x, ay + y, 2.0) for x, y in nodes]
        chord = vbo.VBO(numpy.array(points, 'f'))

        with gl.util.draw_vbo(0, chord):
            GL.glUniform4f(self._loc('flat', 'color'),
                           *self._color('chord', 'bg', type))
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
            GL.glUniform4f(self._loc('flat', 'color'),
                           *self._color('screen', 'fg'))
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)

    def draw_chords(self, nodes):
        if len(nodes) < 3:
            return

        if (0, 0) in nodes:
            if (0, 1) in nodes:
                if (1, 0) in nodes:
                    self.draw_chord([(0, 0), (0, 1), (1, 0)], 'major')
                if (-1, 1) in nodes:
                    self.draw_chord([(0, 0), (0, 1), (-1, 1)], 'minor')

            if (0, -1) in nodes:
                if (1, -1) in nodes:
                    self.draw_chord([(0, 0), (0, -1), (1, -1)], 'major')
                if (-1, 0) in nodes:
                    self.draw_chord([(0, 0), (0, -1), (-1, 0)], 'minor')

            if (-1, 0) in nodes and (-1, 1) in nodes:
                self.draw_chord([(0, 0), (-1, 0), (-1, 1)], 'major')

            if (1, 0) in nodes and (1, -1) in nodes:
                self.draw_chord([(0, 0), (1, 0), (1, -1)], 'minor')

        if (-1, 0) in nodes and (-1, -1) in nodes:
            if (-2, 0) in nodes:
                self.draw_chord([(-1, 0), (-1, -1), (-2, 0)], 'minor')
            if (0, -1) in nodes:
                self.draw_chord([(-1, 0), (-1, -1), (0, -1)], 'major')

        if (1, 1) in nodes:
            if (2, 0) in nodes and (2, 1) in nodes:
                self.draw_chord([(1, 1), (2, 0), (2, 1)], 'minor')
            if (1, 0) in nodes:
                if (2, 0) in nodes:
                    self.draw_chord([(1, 1), (1, 0), (2, 0)], 'major')
                if (0, 1) in nodes:
                    self.draw_chord([(1, 1), (1, 0), (0, 1)], 'minor')

    def draw_arrow(self, src, dst, surface, color):
        s = vector.Vec2(src)
        d = vector.Vec2(dst)

        is_unit = (d - s).norm == 1

        if is_unit:
            is_arc = False
        else:
            is_arc = (s[0] == d[0]) or (s[1] == d[1])

        points = [self._node_coords(*node, center=True)
                  for node in [src, dst]]

        offset = vector.Vec2(self.node_size).norm * 0.175
        path = (-vector.Vec2(points[0]) +
                vector.Vec2(points[1]))

        direction = path.normalized

        points[0] = (vector.Vec2(points[0]) +
                     direction * self.node_radius +
                     direction.normal * 0.2 * self.node_radius).vec
        points[1] = (vector.Vec2(points[1]) -
                     direction * self.node_radius +
                     direction.normal * 0.2 * self.node_radius).vec
        mid = vector.Vec2(points[1]) - (direction * 0.2 * self.node_radius)

        if is_arc:
            points.insert(1, (vector.Vec2(points[1]) -
                              direction * offset +
                              direction.normal * offset).vec)
            points.insert(1, (vector.Vec2(points[0]) +
                              direction * offset +
                              direction.normal * offset).vec)

        points.append((mid + direction.normal * 0.15 * self.node_radius).vec)
        points.append((mid - direction.normal * 0.15 * self.node_radius).vec)
        points.append(points[3 if is_arc else 1])

        pygame.draw.lines(surface,
                          color,
                          False,
                          points,
                          3)

    def draw_trace(self):
        def rgb_from_hsv(h, s, v):
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

            return (r * 255, g * 255, b * 255)

        def color(index, steps):
            return rgb_from_hsv((steps - i % 361),
                                0.75 + index / (4 * steps),
                                0.75 + index / (4 * steps))

        count = len(self.trace)
        trace = pygame.surface.Surface(self.mode,
                                       flags=pygame.SRCALPHA).convert_alpha()

        for i in range(1, count):
            self.draw_arrow(src=self.trace[i - 1],
                            dst=self.trace[i],
                            surface=trace,
                            color=color(i, count - 1))

        self.screen.blit(trace, (0, 0))

    def draw_net(self):
        return
        width, height = self.node_size
        x, y = self._node_coords(*self.tn.anchor)
        offset = min(width, height) - 2.5 * self.node_radius

        points = [(x - width + offset, y - 1 * height + offset),
                  (x - width + offset, y + 0 * height),
                  (x - 2 * width + offset, y + 0 * height),
                  (x - 2 * width + offset, y + 1 * height - offset),
                  (x - width + offset, y + 1 * height - offset),
                  (x - width + offset, y + 2 * height - offset),
                  (x + 2 * width + offset, y + 2 * height - offset),
                  (x + 2 * width + offset, y + 1 * height - offset),
                  (x + 3 * width + offset, y + 1 * height - offset),
                  (x + 3 * width + offset, y - 1 * height + offset),
                  ]

        pygame.draw.polygon(self.screen,
                            self._color('screen', 'hl'),
                            points, 0)

        self.tn.set_active(self.ut.keys)
        self.draw_chords([self.tn.pitch_coordinates(key, relative=True)
                          for key in self.ut.keys])

        for column in range(self.tn.left, self.tn.right + 1):
            for row in range(self.tn.bottom, self.tn.top + 1):
                self.draw_node(column, row)

        pygame.draw.polygon(self.screen,
                            self._color('screen', 'fg'),
                            points, 1)

        self.draw_trace()

    def init_gl(self):
        def compile(name):
            def compile_shader(type):
                with open(self.data(gl.shaders.filename(name, type),
                                    app='vismut')) as shader:
                    return gl.shaders.compile_shader(shader.read(), type)

            vertex = compile_shader(gl.shaders.VERTEX)
            fragment = compile_shader(gl.shaders.FRAGMENT)

            return GL.shaders.compileProgram(vertex, fragment)

        self.programs = {'flat': compile('flat'),
                         'textured': compile('textured'),
                         }

        def uni(prog, name):
            return GL.glGetUniformLocation(self.programs[prog], name)

        def att(prog, name):
            return GL.glGetAttribLocation(self.programs[prog], name)

        self.locs = {'flat': {'color': uni('flat', 'color'),
                              'translation': uni('flat', 'translation'),
                              'transformation': uni('flat', 'transformation'),
                              },
                     'textured': {'texture': uni('textured', 'the_texture'),
                                  'texcoords': att('textured',
                                                   'the_tex_coords'),
                                  'translation': uni('textured',
                                                     'translation'),
                                  'transformation': uni('textured',
                                                        'transformation'),
                                  },
                     }

        GL.glClearColor(*self._color('screen', 'bg'))

    def resize_event(self, event):
        self.aspect = event.w / event.h
        self.resize_net()

    def resize_net(self, growth=None):
        self.matrix = gl.util.ortho(self.tn.left - 0.5,
                                    self.tn.right + 0.5,
                                    self.tn.bottom - 0.5,
                                    self.tn.top + 0.5,
                                    1,
                                    2)

        scale = self.tn.columns / self.tn.rows

        if self.aspect <= 1:
            w, h = (0.5 * self.aspect, 0.5)
        else:
            w, h = (0.5, 0.5 * self.aspect)

        if scale <= 1:
            w /= scale
        else:
            h /= scale

        self.node_size = (w, h)

        self._geometry('node', gl.geometry.circle(center=(0, 0),
                                                  radius=self.node_radius,
                                                  scale=self.node_size,
                                                  subdivisions=5))

        self._geometry('label', gl.geometry.label(center=(0, 0),
                                                  radius=self.node_radius,
                                                  scale=self.node_size))

        self._geometry('cage', gl.geometry.cage(offset=(0.5, 0.45),
                                                scale=self.node_size))

        self._geometry('grid', gl.geometry.grid(self.tn.left, self.tn.right,
                                                self.tn.bottom, self.tn.top))

        self.polys = (self.tn.columns * self.tn.rows *
                      (self.vertices['node'] + self.vertices['label']) +
                      self.vertices['cage'])

        if growth is not None:
            pass                  # TODO: only create the new textures

        for column in range(self.tn.left, self.tn.right + 1):
            for row in range(self.tn.bottom, self.tn.top + 1):
                tex = self._make_label(column, row)
                if column in self.textures:
                    self.textures[column][row] = tex
                else:
                    self.textures[column] = {row: tex,
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
                        growth = self.tn.grow(min_dist=1, by=1)
                        self.resize_net(growth)
                        self.grow_count = 0

        self.draw()

    def draw(self):
        self.tn.set_active(self.ut.keys)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        with gl.util.use_program(self.programs['flat']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('flat',
                                                             'transformation'))
            GL.glUniform3f(self._loc('flat', 'translation'), 0.0, 0.0, 0.0)
            self.draw_chords([self.tn.pitch_coordinates(key, relative=True)
                              for key in self.ut.keys])

            with gl.util.draw_vbo(0, self.vbos['grid']):
                GL.glUniform4f(self._loc('flat', 'color'),
                               *self._color('key', 'bg', 'inactive'))
                GL.glDrawArrays(GL.GL_LINES, 0, self.vertices['grid'])

            color = self._color('screen', 'hl')

            with gl.util.draw_vbo(0, self.vbos['cage']):
                x, y = self.tn.anchor
                GL.glUniform3f(self._loc('flat', 'translation'),
                               x, y, 0.0)
                GL.glUniform4f(self._loc('flat', 'color'), *color)
                GL.glDrawArrays(GL.GL_LINE_STRIP, 0, self.vertices['cage'])

            with gl.util.draw_vbo(0, self.vbos['node']):
                for column in range(self.tn.left, self.tn.right + 1):
                    for row in range(self.tn.bottom, self.tn.top + 1):
                        self.draw_node(column, row)

        with gl.util.use_program(self.programs['textured']) as program:
            gl.util.transformation_matrix(program, self.matrix,
                                          location=self._loc('textured',
                                                             'transformation'))
            with gl.util.draw_vbo(0, self.vbos['label'], stride=20):
                with gl.util.enabled(GL.GL_BLEND):
                    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
                    GL.glUniform1i(self._loc('textured', 'texture'), 0)
                    loc = self._loc('textured', 'texcoords')
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

        utabor.destroy_uTabor()
        sys.exit()
