from pygame import Rect, Vector2

import configuration
from window_engine import draw


class DiagramItem:

    def __init__(self, path: str, center_position: Vector2):
        self.path = path
        self.center_position = center_position
        self.size = (160, 40)
        self.hovered = False
        self.is_child_hovered = False

    def draw(self):
        draw.rect(self.get_rect())

    def get_rect(self) -> Rect:
        rect = Rect(0, 0, 0, 0)
        rect.center = self.center_position
        rect.size = self.size
        return rect

    def get_rect_with_padding(self):
        rect = self.get_rect()
        pad = configuration.item_padding
        return Rect(rect.x + pad, rect.y + pad, rect.w - pad * 2, rect.h - pad * 2)