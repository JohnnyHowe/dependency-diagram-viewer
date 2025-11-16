import pygame
from singleton import Singleton


class FontCache(metaclass=Singleton):
    def __init__(self) -> None:
        self._fonts = {}

    def get_font(self, size: int) -> pygame.font.Font:
        if not size in self._fonts:
            self._create_new(size)
        return self._fonts[size]

    def _create_new(self, size: int):
        self._fonts[size] = pygame.font.SysFont("Comic Sans MS", size)