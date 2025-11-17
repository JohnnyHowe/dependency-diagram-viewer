import math
import pygame
from pygame import Vector2, Rect

from window_engine.camera import Camera
from window_engine.font_cache import FontCache
from window_engine.window import Window


def rect(rect: Rect, color="#ffffff", width=1):
    pygame.draw.rect(Window().surface, color, Camera().project_rect(rect), max(1, int(Camera().project_size_component(width))))


def text(text: str, size: float, containing_rect: Rect, color="#ffffff"):
    text_screen_space(text, int(Camera().project_size_component(size)), Camera().project_rect(containing_rect), color)


def text_screen_space(text: str, size: float, containing_rect: Rect, color="#ffffff"):
    lines = text.splitlines()
    font = FontCache().get_font(int(size))

    real_space_used_with_target_font_size = Vector2(0, 0)
    for line in lines:
        real_space_used_with_target_font_size += Vector2(font.size(line))

    scale_factor = min(containing_rect.width / real_space_used_with_target_font_size.x, containing_rect.height / real_space_used_with_target_font_size.y)
    scale_factor = min(scale_factor, 1)

    real_font_size = math.floor(size * scale_factor)
    font = FontCache().get_font(int(real_font_size))
    
    position = Vector2(containing_rect.topleft)
    for line in lines:
        Window().surface.blit(font.render(line, True, color), position)
        position.y += real_font_size