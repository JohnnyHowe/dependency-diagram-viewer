import pygame
from pygame import Vector2

from window_engine.singleton import Singleton


class Window(metaclass=Singleton):
    surface: pygame.Surface
    size: Vector2 = Vector2(1280, 960)
    pygame_events: list

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._reset_surface()
        self.pygame_events = []

    def update(self):
        self._run_event_loop()
        pygame.display.flip()

    def _run_event_loop(self):
        self.pygame_events = pygame.event.get()
        for event in self.pygame_events:
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.VIDEORESIZE:
                self.size = Vector2(event.w, event.h)
                self._reset_surface()

    def _reset_surface(self):
        self.surface = pygame.display.set_mode(self.size, pygame.RESIZABLE)
