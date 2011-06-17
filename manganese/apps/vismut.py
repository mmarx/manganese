
from __future__ import division

import sys
import os.path

import numpy
import pygame
import pygame.image

import OpenGL

OpenGL.ERROR_CHECKING = not True
OpenGL.ERROR_LOGGING = not True
OpenGL.FULL_LOGGING = False
OpenGL.ERROR_ON_COPY = not True
OpenGL.FORWARD_COMPATIBLE_ONLY = not True

from OpenGL import GL
from OpenGL.arrays import vbo

import _apps

from manganese.vismut import gl
from manganese.vismut import themes

import manganese.vismut.gl.util
import manganese.vismut.gl.context
import manganese.vismut.gl.shaders
import manganese.vismut.gl.geometry
import manganese.vismut.gl.textures

import manganese.utabor._utabor as utabor
import manganese.midi.jack as jack
import manganese.midi.jack.dummy
import manganese.utabor.centered_net as net


class Application(_apps.Application):
    def _color(self, *args, **kwargs):
        return self.theme.color(*args, **kwargs)

    vsync = not not True
    max_fps = 30
    anchor = 60
    grow_count = 0
    node_radius = 0.25
    traced_up_to = 1
    trace_vertices = numpy.array([], 'f').reshape(0, 4)
    trace = [(0, 0),
             ]

    frame = -1

    locs = {}
    vbos = {}
    programs = {}
    textures = {}
    vertices = {}

    def _loc(self, prog, name):
        return self.locs[prog][name]

    def _text(self, the_text, color):
        if not self.font:
            return

        return self.font.render(the_text, True, color)

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

        return gl.textures.node_label(label)

    def init_gl(self):
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

        GL.glClearColor(*self.theme.color('screen', 'bg'))
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self.trace_map = self.theme.trace_colors(steps=128)

    def cleanup_gl(self):
        GL.glDeleteTextures(numpy.array([self.trace_map, self.font_atlas] +
                                        [self.textures[column][row]
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
        self.theme.matrix = self.matrix

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

        self._geometry('trace', [])

        self._geometry('node', gl.geometry.circle(radius=self.node_radius,
                                                  scale=self.node_size,
                                                  subdivisions=5,
                                                  z=0.5))

        self._geometry('label', gl.geometry.label(radius=self.node_radius,
                                                  scale=self.node_size,
                                                  z=0.75))

        outline = list(self.theme.color('screen', 'fg'))
        background = list(self.theme.color('screen', 'hl'))
        self._geometry('cage',
                       gl.geometry.cage(offset=(0.5, 0.45),
                                        scale=self.node_size, z=0.25,
                                        outline=outline,
                                        background=background))

        self._geometry('grid', gl.geometry.grid(self.tn.left, self.tn.right,
                                                self.tn.bottom, self.tn.top,
                                                z=0.125))
        self._geometry('chords',
                       gl.geometry.chords(z=0.45,
                                          major=list(self._color('chord', 'bg',
                                                            'major')),
                                          minor=list(self._color('chord', 'bg',
                                                            'minor')),
                                          outline=outline))

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
        #print '-!- fps:', self.context.clock.get_fps(), 'polys: ', self.polys
        if self.action != 'write-replay' or self.frame >= 0:
            self.frame += 1
            self.client.frame(self.frame)

        eventful = False

        while self.client.have_events:
            if not eventful and self.action == 'write-replay':
                if self.frame < 0:
                    self.frame = 0
                    self.client.frame(self.frame)
                    print >> self.replay_file, "events = {0: [",
                else:
                    print >> self.replay_file, "          %d: [" % self.frame,
            eventful = True
            event = self.client.next_event()

            if len(event.raw) <= 4:
                if self.action == 'write-replay':
                    print >> self.replay_file, ("%s, " % event.raw), 
                    
                self.ut.handle_midi(event.as_dword())

                if self.ut.anchor_changed:
                    anchor = self.ut.anchor
                    if anchor != self.anchor:
                        self.tn.move(anchor)
                        self.anchor = anchor
                        if self.trace[-1] != self.tn.anchor:
                            self.trace.append(self.tn.anchor)

                if self.tn.should_grow(min_dist=1):
                    self.tn.grow(min_dist=1, by=1)
                    self.resize_net()

        if eventful and self.action == 'write-replay':
            print >> self.replay_file, "],"

        self.theme.draw()

        if self.action == 'dump-frames':
            # dump frame here
            frame = GL.glReadPixels(0,
                                    0,
                                    self.mode[0],
                                    self.mode[1],
                                    GL.GL_RGBA,
                                    GL.GL_UNSIGNED_BYTE)

            surface = pygame.image.fromstring(frame, self.mode, "RGBA", True)
            pygame.image.save(surface,
                              os.path.join(self.dump_prefix,
                                           '%06d.tga' % self.frame))            
            if self.frame >= self.client.last_frame():
                self.context.quit_handler(None)

    def run(self):
        self.action = self.cfg('action', 'live')

        replay_file = self.cfg('replay-file', None)

        if self.action in ['replay', 'write-replay', 'dump-frames']:
            if replay_file:
                replay_file = os.path.expanduser(replay_file)
                if self.action == 'write-replay':
                    self.replay_file = open(replay_file, 'w')
                else:
                    self.replay_file = replay_file
            else:
                print "-!-", "Need a replay-file."
                sys.exit(1)

            if self.action == 'dump-frames':
                self.max_fps = 0
                dump_prefix = self.cfg('dump-prefix', None)

                if not dump_prefix:
                    print "-!-", "Need a dump-prefix."
                    sys.exit(1)
                else:
                    self.dump_prefix = os.path.expanduser(dump_prefix)
        
        self.tn = net.ToneNet(**self.cfg('net', {}))

        self.context = gl.context.OpenGLContext(renderer=self.render,
                                                max_fps=self.max_fps,
                                                vsync=self.vsync)

        mode = self.cfg('mode', (640, 480))
        self.mode = mode
        self.context.setup(mode)
        self.aspect = mode[0] / mode[1]

        self.font = pygame.font.SysFont(name=self.cfg('font',
                                                      'bitstreamverasans'),
                                        size=self.cfg('font_size', 12),
                                        bold=False,
                                        italic=False)
        self.font_atlas = gl.textures.font_atlas(self.data('vera.ttf',
                                                           app='vismut'),
                                                 0, 128)

        self.ut = utabor.get_uTabor()
        logic = os.path.join(self.prefix(), 'data', 'utabor', 'demo.mut')
        self.ut.load_logic(logic)
        self.ut.select_action('N', True)

        self.theme = themes.get(self.cfg('theme', 'default'), self)
        self.resize_net()

        self.init_gl()

        self.context.add_handler(pygame.VIDEORESIZE, self.resize_event)

        if self.action not in ['replay', 'dump-frames']:
            client_factory = jack.create_client
        else:
            events = dict()
            execfile(self.replay_file, dict(), events)
            
            if 'events' not in events:
                print "-!-", "Invalid replay file."
                sys.exit(1)
                
            client_factory = jack.dummy.create_client(**events)

        with client_factory() as jack_client:
            self.client = jack_client

            self.context.run()

        self.cleanup_gl()

        if self.action == 'write-replay':
            print >> self.replay_file, "}"
            self.replay_file.close()

        utabor.destroy_uTabor()
        sys.exit()
