
from __future__ import division

import sys
import os.path

import pygame

import _apps

import manganese.utabor._utabor as utabor
import manganese.midi.pitch as pitch
import manganese.utabor.net as net


class Application(_apps.Application):

    midi0 = [0x00513090,
             0x00513490,
             0x00513790,
             0x00003080,
             0x00003480,
             0x00003780,
             0x00512d90,
             0x00513190,
             0x00513490,
             0x00002d80,
             0x00003180,
             0x00003480,
            ]

    midi1 = [0x00513090,
             0x00513490,
             0x00513790,
             0x00003080,
             0x00003480,
             0x00003780,
             0x00512d90,
             0x00513090,
             0x00513490,
             0x00002d80,
             0x00003080,
             0x00003480,
            ]

    midi2 = [0x00513090,
             0x00513490,
             0x00513790,
             0x00003080,
             0x00003480,
             0x00003780,
             0x00513290,
             0x00513590,
             0x00513990,
             0x00003280,
             0x00003580,
             0x00003980,
             0x00513590,
             0x00513990,
             0x00513c90,
             0x00003580,
             0x00003980,
             0x00003c80,
             0x00513790,
             0x00513b90,
             0x00513e90,
             0x00003780,
             0x00003b80,
             0x00003e80,
             0x00513c90,
             0x00514090,
             0x00514390,
             0x00003c80,
             0x00004080,
             0x00004380,
            ]

    midi = midi0

    default_colors = {'screen_bg': (0, 0, 0),
                      'screen_fg': (255, 255, 255),
                      'key_bg': {'active': (255, 0, 0),
                                 'inactive': (200, 0, 0),
                                 'anchor': (200, 150, 150),
                                 'anchor_active': (255, 200, 200),
                                 },
                      'key_fg': (255, 255, 255),
                      'chord_bg': {'major': (255, 255, 0),
                                   'minor': (0, 255, 255),
                                   },
                      }

    rows = 7
    max_fps = 60
    once = True

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

    def _coord(self, x, y, rect=None):
        if rect is not None:
            abs_x, abs_y = rect
        else:
            abs_x, abs_y = self.mode

        return (int(x * abs_x), int(y * abs_y))

    def _pitch_index(self, row, column):
        return column * 7 + 4 * (row - 1)

    def _pitch(self, row, column):
        pitches = [
            ['his', 'fisis', 'cisis', 'gisis', 'disis', 'aisis', 'eisis', 'hisis', 'fisisis', 'cisisis', 'gisisis', 'disisis', 'aisisis', 'eisisis'],
            ['gis', 'dis', 'ais', 'eis', 'his', 'fisis', 'cisis', 'gisis', 'disis', 'aisis', 'eisis', 'hisis', 'fisisis', 'cisisis'],
            ['e', 'h', 'fis', 'cis', 'gis', 'dis', 'ais', 'eis', 'his', 'fisis', 'cisis', 'gisis', 'disis', 'aisis'],
            ['c', 'g', 'd', 'a', 'e', 'h', 'fis', 'cis', 'gis', 'dis', 'ais', 'eis', 'his', 'fisis'],
            ['as', 'es', 'b', 'f', 'c', 'g', 'd', 'a', 'e', 'h', 'fis', 'cis', 'gis', 'dis'],
            ['fes', 'ces', 'ges', 'des', 'as', 'es', 'b', 'f', 'c', 'g', 'd', 'a', 'e', 'h'],
            ['deses', 'asas', 'eses', 'heses', 'fes', 'ces', 'ges', 'des', 'as', 'es', 'b', 'f', 'c', 'g'],
            ['heses', 'feses', 'ceses', 'geses', 'deses', 'asas', 'eses', 'heses', 'fes', 'ces', 'ges', 'des', 'as', 'es'],
            ['geseses', 'deseses', 'asasas', 'eseses', 'heseses', 'feses', 'ceses', 'geses', 'deses', 'asas', 'eses', 'heses', 'fes', 'ces'],
            ]

        return pitches[(4 - row)][column]

        classifier = self.tn.pitchClassifier

        if row > 0 or (row == 0 and column >= 3):
            augment = True
        else:
            augment = False

        return classifier.name(classifier.classify(
            self._pitch_index(row, column)), augment=augment)

    def _coord_from_midi(self, midi):
        row = ((midi - 60) // 12) - 1
        pitch = midi % 12
        column = (7 * pitch - 4 * (row - 1)) % 12

        return (row, column)

    def _node_type(self, row, column):
        anchor = y, x = self._coord_from_midi(self.ut.anchor)

        is_anchor = False

        if anchor == (row, column):
            is_anchor = True

        for key in self.ut.keys:
            rel_x, rel_y = self.tn.coordinates((key - (self.ut.anchor % 12))
                                               % 12)

            if ((x + rel_x) % 13, y + rel_y) == (column, row):
                if is_anchor:
                    return 'anchor_active'
                else:
                    return 'active'

        if is_anchor:
            return 'anchor'

        return 'inactive'

    def draw_node(self, row, column):
        size = width, height = self._coord(1 / 14, 1 / self.rows)
        node = pygame.surface.Surface(size, flags=pygame.SRCALPHA).convert()

        radius = 3 * min(width, height) // 8
        color = self._color('key', 'bg', self._node_type(row, column))
        center = x, y = self._coord(0.5, 0.5, size)

        pygame.draw.circle(node, color, center, radius)
        pygame.draw.line(node, color, (0, y), ((width - x), y))
        pygame.draw.line(node, color, ((width - x), y), (width, y))
        pygame.draw.line(node, color, (x, 0), (x, (height - y)))
        pygame.draw.line(node, color, (x, (height - y)), (x, height))

        x = column / 14
        y = 0.5 - ((row + (self.rows % 2) * 0.5) / self.rows)

        color = self._color('key', 'fg')

        label = self._text(self._pitch(row, column), color)
        node.blit(label, label.get_rect(center=center))

        self.screen.blit(node, self._coord(x, y))

    def draw_row(self, row):
        for column in range(14):
            self.draw_node(row, column)

    def draw_net(self):
        rows = self.rows
        next_row = 0

        while rows > 0:
            self.draw_row(next_row)

            if(next_row >= 0):
                next_row = -abs(next_row) - 1
            else:
                next_row *= -1

            rows -= 1

    def run(self):
        pygame.init()

        self.mode = self._parse_mode(self.cfg('mode', '640x480'))
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
        print '-!- initial tone net:'
        self.tn = net.ToneNet(pitch.PitchClassifier(naming=pitch.NamingDE))
        self.tn.print_net()
        print
        self.ut.keys

        running = True

        midi_current = -1
        midi_frames = self.max_fps + 1

        while running:
            self.clock.tick(self.max_fps)
            midi_frames += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.mode = (event.w, event.h)

            if midi_frames > self.max_fps:
                midi_frames = 0
                midi_current = (midi_current + 1)

                if midi_current >= len(self.midi):
                    if self.once:
                        running = False
                        continue
                    else:
                        midi_current = 0

                self.ut.handle_midi(self.midi[midi_current])

                if self.ut.anchor_changed:
                    self.tn.move(self.ut.anchor)

                if self.ut.need_update:
                    self.tn.print_net(mark=self.ut.keys)
                    print

            self.screen.fill(self._color('screen', 'bg'))
            self.draw_net()
            pygame.display.flip()

        utabor.destroy_uTabor()
        sys.exit()
