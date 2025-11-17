from pygame import Rect, Vector2

import configuration
from window_engine import draw


class DiagramItem:

    def __init__(self, path: str, name: str, center_position: Vector2):
        self.path = path
        self.name = name
        
        self.hovered = False
        self.is_child_hovered = False

        self.rect = Rect(0, 0, 0, 0)
        self.rect.center = center_position
        self.rect.size = Vector2(160, 40)

    def draw(self):
        draw.rect(self.get_rect())

    def get_rect(self) -> Rect:
        return self.rect

    def get_rect_with_padding(self):
        rect = self.get_rect()
        pad = configuration.padding
        return Rect(rect.x + pad, rect.y + pad, rect.w - pad * 2, rect.h - pad * 2)