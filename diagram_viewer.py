import pygame
from pygame import Vector2

import draw
from window import Window
from camera_controller import CameraController

class DiagramViewer:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._camera_controller = CameraController()
        self._run()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._camera_controller.update()
        self._draw()
        Window().update()

    def _draw(self):
        Window().surface.fill((0, 0, 0))
        draw.rect(pygame.Rect(-100, -100, 200, 200))
        self._draw_controls_text()

    def _draw_controls_text(self):
        draw.text_screen_space("hold middle mouse to pan\nscrollwheel to zoom\n\nf: reset camera", 20, Vector2(0, 0))