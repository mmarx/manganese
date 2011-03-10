
from __future__ import division

import sys
import os.path

import pygame

import _apps

import manganese.utabor._utabor as utabor
import manganese.midi.pitch as pitch
import manganese.midi.jack as jack
import manganese.utabor.centered_net as net


class Application(_apps.Application):

    default_colors = {'screen_bg': (255, 255, 255),
                      'screen_fg': (0, 0, 0),
                      'key_bg': {'active': (180, 220, 250),
                                 'inactive': (180, 180, 250),
                                 'anchor': (220, 180, 250),
                                 'anchor_active': (220, 220, 250),
                                 },
                      'key_fg': (80, 80, 80),
                      'chord_bg': {'major': (255, 255, 0),
                                   'minor': (255, 200, 0),
                                   },
                      }

    max_fps = 60
    anchor = 60

    def _parse_mode(self, mode):
        if isinstance(mode, basestring):
            return [int(x) for x in mode.split('x')]
        return mode

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

    def _node_type(self, x, y):
        is_anchor = self.tn.is_anchor(x, y)

        if self.tn.is_active(x, y):
                if is_anchor:
                    return 'anchor_active'
                else:
                    return 'active'

        if is_anchor:
            return 'anchor'

        return 'inactive'

    def draw_node(self, column, row):
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

        x, y = self._node_at(column, row)

        color = self._color('key', 'fg')

        label = self._text(self.tn.name(column, row), color)
        node.blit(label, label.get_rect(center=self.node_center))

        self.screen.blit(node, self._coord(x, y))

    def draw_chord(self, nodes, type):
        ax, ay = self.tn.anchor
        points = [self._coord(*self._node_at(ax + x, ay + y), center=True)
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

    def draw_net(self):
        self.tn.set_active(self.ut.keys)
        self.draw_chords([self.tn.pitch_coordinates(key, relative=True)
                          for key in self.ut.keys])

        for column in range(self.tn.left, self.tn.right + 1):
            for row in range(self.tn.bottom, self.tn.top + 1):
                self.draw_node(column, row)

        width, height = self.node_size
        x, y = self._coord(*self._node_at(*self.tn.anchor))
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
                            self._color('screen', 'fg'),
                            points, 1)

    def resize(self, mode):
        self.mode = mode
        self.node_size = width, height = self._coord(1 / self.tn.columns,
                                                     1 / self.tn.rows)
        self.node_radius = 3 * min(width, height) // 8
        self.node_center = x, y = self._coord(0.5, 0.5, self.node_size)

    def run(self):
        self.tn = net.ToneNet()

        pygame.init()

        self.resize(self._parse_mode(self.cfg('mode', '640x480')))
        self.screen = pygame.display.set_mode(self.mode)

        self.colors = self.cfg('colors', self.default_colors)
        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)
        self.clock = pygame.time.Clock()

        self.ut = utabor.get_uTabor()
        logic = os.path.join(self.prefix(), 'data', 'utabor', 'demo.mut')
        self.ut.load_logic(logic)
        self.ut.select_action('N', True)
        print
        self.ut.keys

        running = True

        with jack.create_client() as jack_client:
            while running:
                self.clock.tick(self.max_fps)

                eventful = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    elif event.type == pygame.VIDEORESIZE:
                        self.resize((event.w, event.h))

                while jack_client.have_events:
                    event = jack_client.next_event()

                    if len(event.raw) <= 4:
                        self.ut.handle_midi(event.as_dword())

                        if self.ut.anchor_changed:
                            anchor = self.ut.anchor
                            if anchor != self.anchor:
                                self.tn.move(anchor)
                                self.anchor = anchor

                            if self.tn.should_grow(min_dist=1):
                                self.tn.grow(min_dist=1, by=1)
                                self.resize(self.mode)

                self.screen.fill(self._color('screen', 'bg'))
                self.draw_net()
                pygame.display.flip()

        utabor.destroy_uTabor()
        sys.exit()
