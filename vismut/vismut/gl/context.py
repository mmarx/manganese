
import pygame


class OpenGLContext(object):
    """A basic OpenGL context using pygame

    This sets up an OpenGL context and provides basic event handling support.
    """

    def __init__(self, renderer, max_fps=60, vsync=True):
        """Construct an OpenGL context

        renderer is a callback used to render the scene.
        The frame rate will be limited to at most max_fps frames per second.
        """
        self.vsync = vsync
        self.running = False
        self.max_fps = max_fps
        self.handlers = {pygame.QUIT: [lambda e: self.quit_handler(e)],
                         pygame.KEYDOWN: [lambda e: self.key_handler(e)],
                         }
        self.render = renderer

    def _parse_mode(self, mode):
        """Try to parse a video mode description

        If mode is a string, it will be interpreted as `<width>x<height>.'
        If mode is a tuple, it must be of the form `(width, height).'

        ValueError is raised on malformed input.
        """
        if isinstance(mode, basestring):
            if mode.count('x') != 1:
                raise ValueError('malformed mode string')

            return [int(x) for x in mode.split('x')]
        elif isinstance(mode, tuple):
            if len(mode) != 2:
                raise ValueError('malformed mode tuple')

            return mode
        else:
            raise ValueError('malformed mode')

    def setup(self, mode):
        """Set up the OpenGL context
        """
        pygame.init()
        the_mode = self._parse_mode(mode)

        try:
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL,
                                            1 if self.vsync else 0)
        except:
            pass  # GL_SWAP_CONTROL might not be available, ignore
        flags = pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF

        self.screen = pygame.display.set_mode(the_mode, flags)
        self.clock = pygame.time.Clock()

    def handle_event(self, event):
        """Generic event handler
        """
        if event.type not in self.handlers:
            return

        for handler in self.handlers[event.type]:
            proceed = handler(event)

            if not proceed:
                return

    def quit_handler(self, _):
        """Default handler for QUIT events
        """
        self.running = False

    def key_handler(self, event):
        """Default handler for KEYDOWN events

        This simply quits on ESCAPE events.
        """
        if event.key == pygame.K_ESCAPE:
            self.running = False

    def add_handler(self, event_type, handler):
        """Add an event handler for a given type

        The handler will be called with the event data as it's only argument.
        """
        if event_type not in self.handlers:
            self.handlers[event_type] = [handler]
        else:
            self.handlers[event_type].insert(0, handler)

    def run(self):
        """Main event loop
        """
        self.running = True

        while self.running:
            self.clock.tick(self.max_fps)

            for event in pygame.event.get():
                self.handle_event(event)

            self.render()

            pygame.display.flip()
