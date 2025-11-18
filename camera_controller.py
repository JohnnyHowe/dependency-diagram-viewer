import math
from pygame import Vector2
import pygame
from window_engine.camera import Camera
from window_engine.mouse import Mouse
from window_engine.window import Window


class CameraController:
    button_number = 1
    reset_key = pygame.K_f
    _zoom_step: int 

    def __init__(self) -> None:
        if not pygame.get_init():
            pygame.init()
        self._zoom_step = 0

    def update(self):
        self._mouse_movement(Mouse().screen_rel)
        self._step_zoom(Mouse().wheel_change)

        for event in Window().pygame_events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.reset_key:
                    self._reset()

    def _step_zoom(self, step_change: int):
        if step_change == 0: return

        mouse_screen_position = Vector2(pygame.mouse.get_pos())
        original_mouse_world_position = Camera().unproject_position(mouse_screen_position)

        self._zoom_step += step_change
        Camera().zoom = self._get_zoom()

        new_mouse_world_position = Camera().unproject_position(mouse_screen_position)
        mouse_position_change = new_mouse_world_position - original_mouse_world_position
        mouse_position_change_screen_size = Camera().project_size(mouse_position_change)

        Camera().position -= mouse_position_change_screen_size

    def _get_zoom(self) -> float:
        return math.pow(1.1, self._zoom_step)

    def _mouse_movement(self, change: Vector2):
        if Mouse().buttons_held[self.button_number]:
            Camera().position -= change

    def _reset(self):
        Camera().position = Vector2(0, 0)
        self._zoom_step = 0
        Camera().zoom = 1