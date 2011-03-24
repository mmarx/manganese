
from __future__ import division

import sys
import math
import os.path

import numpy
import pygame

import OpenGL

OpenGL.FULL_LOGGING = True
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

    default_colors = {'screen_bg': (255, 255, 255),
                      'screen_fg': (0, 0, 0),
                      'screen_hl': (50, 230, 230),
                      'key_bg': {'active': (200, 230, 250),
                                 'inactive': (160, 160, 220),
                                 'anchor': (250, 200, 250),
                                 'anchor_active': (220, 220, 250),
                                 'anchor_initial': (200, 0, 0),
                                 'anchor_initial_active': (255, 0, 0),
                                 },
                      'key_fg': (80, 80, 80),
                      'chord_bg': {'major': (255, 255, 0),
                                   'minor': (255, 200, 0),
                                   },
                      }

    vsync = True
    max_fps = 60
    anchor = 60
    grow_count = 0
    trace = [(0, 0),
             ]

    def _compile_shader(self, name, type):
        with open(self.data(gl.shaders.filename(name, type),
                            app='vismut')) as shader:
            return gl.shaders.compile_shader(shader.read(), type)

    def _compile_program(self, name):
        vertex = self._compile_shader(name, gl.shaders.VERTEX)
        fragment = self._compile_shader(name, gl.shaders.FRAGMENT)

        return GL.shaders.compileProgram(vertex, fragment)

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

    def _coord(self, x, y, rect=None, center=False):
        if rect is not None:
            abs_x, abs_y = rect
        else:
            abs_x, abs_y = self.mode

        if center:
            off_x, off_y = self.node_size            
            off_x *= 0.5
            off_y *= 0.5
        else:
            off_x = off_y = 0

        return (int(x * abs_x + off_x), int(y * abs_y + off_y))

    def _node_at(self, x, y):
        nx = x - self.tn.left
        ny = self.tn.top - y

        return ((nx / self.tn.columns), (ny / self.tn.rows))

    def _node_coords(self, x, y, **kwargs):
        return self._coord(*self._node_at(x, y), **kwargs)

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

    def draw_node(self, column, row):
        loc = GL.glGetUniformLocation(self.program, 'translation')

        with gl.util.bind(self.node_vbo):
            GL.glEnableVertexAttribArray(0)
            GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, False, 0, self.node_vbo)
            GL.glUniform3f(loc, column, row, 0)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.node_vertices)
            GL.glDisableVertexAttribArray(0)

        return
        width, height = self.node_size
        x, y = self.node_center
        node = pygame.surface.Surface(self.node_size,
                                      flags=pygame.SRCALPHA).convert_alpha()
        node.fill((0, 0, 0, 0))

        color = self._color('key', 'bg', self._node_type(column, row))

        pygame.draw.circle(node, color, self.node_center, self.node_radius)
        pygame.draw.line(node, color, (0, y), ((width - x), y))
        pygame.draw.line(node, color, ((width - x), y), (width, y))
        pygame.draw.line(node, color, (x, 0), (x, (height - y)))
        pygame.draw.line(node, color, (x, (height - y)), (x, height))

        color = self._color('key', 'fg')

        label = self._text(self.tn.name(column, row), color)
        node.blit(label, label.get_rect(center=self.node_center))

        self.screen.blit(node, self._node_coords(column, row))

    def draw_chord(self, nodes, type):
        ax, ay = self.tn.anchor
        points = [self._node_coords(ax + x, ay + y, center=True)
                  for x, y in nodes]

        pygame.draw.polygon(self.screen,
                            self._color('chord', 'bg', type),
                            points, 0)
        pygame.draw.polygon(self.screen,
                            self._color('screen', 'fg'),
                            points, 1)

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

    def resize_event(self, event):
        self.aspect = event.w / event.h
        self.resize_net()

    def resize_net(self):
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

        node_vertices = gl.geometry.circle(center=(0, 0),
                                           radius=.5,
                                           scale=self.node_size,
                                           subdivisions=5)
        self.node_vbo = vbo.VBO(numpy.array(node_vertices, 'f'))
        self.node_vertices = len(node_vertices)

    def render(self):
        print '-!- fps: ', self.context.clock.get_fps()
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
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        with gl.util.use_program(self.program) as program:
            gl.util.transformation_matrix(program, self.matrix)

            for column in range(self.tn.left, self.tn.right + 1):
                for row in range(self.tn.bottom, self.tn.top + 1):
                    self.draw_node(column, row)                

    def run(self):
        self.tn = net.ToneNet()

        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps,
                                                vsync=self.vsync)

        mode = self.cfg('mode', '640x480')
        self.context.setup(mode)
        self.aspect = mode[0] / mode[1]
        self.resize_net()        

        self.colors = self.cfg('colors', self.default_colors)
        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)

        self.ut = utabor.get_uTabor()
        logic = os.path.join(self.prefix(), 'data', 'utabor', 'demo.mut')
        self.ut.load_logic(logic)
        self.ut.select_action('N', True)

        self.program = self._compile_program('simple')

        self.context.add_handler(pygame.VIDEORESIZE, self.resize_event)

        with jack.create_client() as jack_client:
            self.client = jack_client

            self.context.run()

        utabor.destroy_uTabor()
        sys.exit()
