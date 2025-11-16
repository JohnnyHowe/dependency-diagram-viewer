import pygame

import draw
from window import Window

class DiagramViewer:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._run()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._draw()
        Window().update()

    def _draw(self):
        Window().surface.fill((0, 0, 0))
        draw.rect(pygame.Rect(-100, -100, 200, 200))