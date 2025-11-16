from pygame import Vector2
import pygame


class CameraController:
    button_number = 0
    _last_mouse_position: Vector2
    _last_pressed_state: bool

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()

    def update(self):
        self._last_mouse_position = Vector2(pygame.mouse.get_pos())
        self._last_pressed_state = pygame.mouse.get_pressed()[self.button_number]