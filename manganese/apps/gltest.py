
import pygame

from OpenGL import GL
from OpenGL.arrays import vbo

import _apps


class Application(_apps.Application):
    max_fps = 60

    def run(self):
        pygame.init()

        flags = pygame.HWSURFACE | pygame.OPENGL | pygame.DOUBLEBUF

        self.screen = pygame.display.set_mode((640, 480), flags)
        self.clock = pygame.time.Clock()

        running = True

        while running:
            self.clock.tick(self.max_fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            pygame.display.flip()
