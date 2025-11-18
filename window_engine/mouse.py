from pygame import Vector2
import pygame
from window_engine.camera import Camera
from window_engine.singleton import Singleton
from window_engine.window import Window


class Mouse(metaclass=Singleton):
    def __init__(self):
        self.screen_position = Vector2(0, 0)
        self.position = Vector2(0, 0)
        self.rel = Vector2(0, 0)
        self.screen_rel = Vector2(0, 0)
        self.buttons_held = [0, 0, 0]
        self.wheel_change = 0

    def update(self):
        self.screen_position = pygame.mouse.get_pos()
        self.position = Camera().unproject_position(self.screen_position)

        self.screen_rel = Vector2(pygame.mouse.get_rel())
        self.rel = Camera().unproject_size(self.screen_rel)

        self.buttons_held = pygame.mouse.get_pressed()

        self.wheel_change = 0
        for event in Window().pygame_events:
            if event.type == pygame.MOUSEWHEEL:
                self.wheel_change = event.y