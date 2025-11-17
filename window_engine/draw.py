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


def text_screen_space(text: str, size: int, containing_rect: Rect, color="#ffffff"):
    max_font_size = _get_max_font_size_for_text_to_fit(text, Vector2(containing_rect.size))
    font_size = min(max_font_size, size)
    font = FontCache().get_font(font_size)
    
    current_position = Vector2(containing_rect.topleft)
    for line in text.splitlines():
        Window().surface.blit(font.render(line, True, color), current_position)
        current_position.y += font_size


def _get_max_font_size_for_text_to_fit(text: str, area: Vector2) -> int:
    n_lines = len(text.splitlines())
    start_size_guess = area.y / n_lines

    space_used =_get_space_rendered_text_will_use(text, start_size_guess) 
    scale_factor = min(area.x / space_used.x, area.y / space_used.y)
    scale_factor = min(scale_factor, 1)

    real_font_size = math.floor(start_size_guess * scale_factor)
    return real_font_size
 

def _get_space_rendered_text_will_use(text: str, screen_font_size: int) -> Vector2:
    font = FontCache().get_font(int(screen_font_size))
    real_space_used_with_target_font_size = Vector2(0, 0)
    for line in text.splitlines():
        real_space_used_with_target_font_size += Vector2(font.size(line))
    return real_space_used_with_target_font_size
