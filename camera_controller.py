from pygame import Vector2
import pygame
from camera import Camera


class CameraController:
    button_number = 1
    _last_mouse_position: Vector2

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._last_mouse_position = Vector2(0, 0)

    def update(self):
        new_position = Vector2(pygame.mouse.get_pos())

        if pygame.mouse.get_pressed()[self.button_number]:
            Camera().position -= new_position - self._last_mouse_position

        self._last_mouse_position = new_position

