import pygame

from camera import Camera
from window import Window


def rect(rect: pygame.Rect, color="#ffffff", width=1):
    pygame.draw.rect(Window().surface, color, Camera().project_rect(rect), max(1, int(Camera().project_size_component(width))))