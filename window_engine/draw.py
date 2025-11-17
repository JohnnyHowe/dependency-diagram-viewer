import pygame
from pygame import Vector2, Rect

from window_engine.camera import Camera
from window_engine.font_cache import FontCache
from window_engine.window import Window


def rect(rect: Rect, color="#ffffff", width=1):
    pygame.draw.rect(Window().surface, color, Camera().project_rect(rect), max(1, int(Camera().project_size_component(width))))


def text(text: str, size: float, position: Vector2, color="#ffffff"):
    text_screen_space(text, int(Camera().project_size_component(size)), Camera().project_position(position), color)


def text_screen_space(text: str, size: int, position: Vector2, color="#ffffff"):
    position = Vector2(position)
    lines = text.splitlines()
    font = FontCache().get_font(size)

    for line in lines:
        Window().surface.blit(font.render(line, True, color), position)
        position.y += size