import pygame
from pygame import Vector2

from singleton import Singleton


class Window(metaclass=Singleton):
    surface: pygame.Surface
    size: Vector2 = Vector2(1280, 960)
    pygame_events: list

    def __init__(self) -> None:
        pygame.init()
        self.surface = pygame.display.set_mode(self.size)

    def update(self):
        self._run_event_loop()
        pygame.display.flip()

    def _run_event_loop(self):
        self.pygame_events = pygame.event.get()
        for event in self.pygame_events:
            if event.type == pygame.QUIT:
                quit()