import math
import pygame
from pygame import Vector2, Rect

from window_engine.camera import Camera
from window_engine.font_cache import FontCache
from window_engine.window import Window


def rect(rect: Rect, color="#ffffff", width=1):
    pygame.draw.rect(Window().surface, color, Camera().project_rect(rect), max(1, int(Camera().project_size_component(width))))


def text(text: str, size: float, containing_rect: Rect, color="#ffffff", v_alignment=-1, h_alignment=-1):
    text_screen_space(text, int(Camera().project_size_component(size)), Camera().project_rect(containing_rect), color, v_alignment, h_alignment)


def text_screen_space(text: str, size: int, containing_rect: Rect, color="#ffffff", v_alignment=-1, h_alignment=-1):
    max_font_size = _get_max_font_size_for_text_to_fit(text, Vector2(containing_rect.size))
    font_size = min(max_font_size, size)
    font = FontCache().get_font(font_size)

    text_area_size = _get_space_rendered_text_will_use(text, font_size)
    current_position = _get_position_for_alignment(containing_rect, text_area_size, v_alignment, h_alignment) 
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


def _get_position_for_alignment(containing_rect: Rect, item_size: Vector2, v_alignment, h_alignment) -> Vector2:
    assert(v_alignment in [-1, 0, 1] and h_alignment in [-1, 0, 1], f"Text alignment values can only be -1, 0, or 1! Recieved {(v_alignment, h_alignment)}.")

    position = Vector2(containing_rect.topleft)
    size_difference = Vector2(containing_rect.size) - item_size

    if h_alignment == 0:
        position.x += size_difference.x / 2
    elif h_alignment == 1:
        position.x += size_difference.x

    if v_alignment == 0:
        position.y += size_difference.y / 2
    elif v_alignment == 1:
        position.y += size_difference.y

    return position