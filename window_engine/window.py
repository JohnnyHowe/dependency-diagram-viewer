import pygame
from pygame import Vector2

from window_engine.singleton import Singleton


class Window(metaclass=Singleton):
    surface: pygame.Surface
    size: Vector2 = Vector2(1280, 960)
    pygame_events: list
    delta_time_seconds: float

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._reset_surface()
        self.pygame_events = []
        self._draw_calls = []
        self._clock = pygame.time.Clock()
        self.delta_time_seconds = 1.0 / 60

    def update(self):
        self.delta_time_seconds = self._clock.tick(120) / 1000.0
        self._run_event_loop()
        for func in sorted(self._draw_calls, key=lambda call: call[1]):
            func[0]()
        self._draw_calls = []
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

    def queue_draw_call(self, draw_func, layer):
        self._draw_calls.append((draw_func, layer))