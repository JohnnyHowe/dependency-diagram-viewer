from pygame import Vector2
import pygame


class CameraController:
    button_number = 0
    _last_mouse_position: Vector2
    _last_pressed_state: bool

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._last_pressed_state = False
        self._last_mouse_position = Vector2(0, 0)

    def update(self):
        new_position = Vector2(pygame.mouse.get_pos())
        new_pressed_state = pygame.mouse.get_pressed()[self.button_number]

        if new_pressed_state and not self._last_pressed_state:
            self._mouse_down()
        elif not new_pressed_state and self._last_pressed_state:
            self._mouse_up()

        self._last_mouse_position = new_position 
        self._last_pressed_state = new_pressed_state

    def _mouse_up(self):
        print("mouse up")

    def _mouse_down(self):
        print("mouse down")

