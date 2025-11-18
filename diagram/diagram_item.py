from pygame import Rect, Vector2

import configuration
from window_engine import draw


class DiagramItem:

    def __init__(self, path: str, name: str, parent, center_position: Vector2):
        self.parent = parent
        self.path = path
        self.name = name
        
        self.is_held = False
        self.is_hovered = False

        self.rect = Rect(0, 0, 0, 0)
        self.rect.center = center_position
        self.rect.size = Vector2(160, 40)

        self.depth = self._get_depth()
        self.is_root = parent == None

    def _get_depth(self) -> int:
        return len(self._get_parent_chain())

    def _get_parent_chain(self) -> list:
        chain = [self]
        while chain[-1].parent:
            chain.append(chain[-1].parent)
        chain.reverse()
        return chain
    
    def move(self, change: Vector2):
        self.rect.topleft = Vector2(self.rect.topleft) + change

    def draw(self):
        draw.rect(self.rect)

    def get_rect_with_padding(self):
        rect = self.rect
        pad = configuration.padding
        return Rect(rect.x + pad, rect.y + pad, rect.w - pad * 2, rect.h - pad * 2)

    def draw_background_fill(self):
        if self.is_held:
            draw.rect(self.rect, configuration.held_item_fill_color, 0)
        elif self.is_hovered:
            draw.rect(self.rect, configuration.hovered_item_fill_color, 0)