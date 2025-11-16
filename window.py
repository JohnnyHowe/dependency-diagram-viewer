import pygame
from pygame import Vector2


class Window:
    file_path: str
    surface: pygame.Surface
    surface_size: Vector2 = Vector2(1280, 960)

    def __init__(self, file_path: str):
        self.file_path = file_path

        pygame.init()
        self.surface = pygame.display.set_mode(self.surface_size)

        self._run()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._run_event_loop()
        self._draw()

    def _run_event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def _draw(self):
        self.surface.fill((0, 0, 0))
        pygame.display.flip()