from pygame import Color, Rect, Vector2

import configuration
from window_engine import draw
from window_engine.window import Window


class DiagramItem:

    def __init__(self, path: str, name: str, parent):
        self.parent = parent
        self.path = path
        self.name = name
        
        self.is_held = False
        self.is_hovered = False

        self.rect = Rect(0, 0, 0, 0)
        self.rect.size = Vector2(160, 40)

        self.depth = self._get_depth()
        self.is_root = parent == None

        self.is_hidden = False
   
    def move(self, change: Vector2):
        self.rect.topleft = Vector2(self.rect.topleft) + change

    # ===========================================================================================
    # region Drawing 
    # ===========================================================================================

    def draw(self):
        draw.rect(self.rect, configuration.item_outline_color)
        self.draw_background_fill()

    def get_rect_with_padding(self):
        rect = self.rect
        pad = configuration.padding
        return Rect(rect.x + pad, rect.y + pad, rect.w - pad * 2, rect.h - pad * 2)

    def draw_background_fill(self):
        color = self.get_fill_color()
        if color:
            draw.rect(self.rect, color, 0)

    def get_fill_color(self) -> Color:
        if self.is_held:
            return configuration.held_item_fill_color
        if self.is_hovered:
            return configuration.hovered_item_fill_color

    def get_outline_color(self) -> Color:
        return configuration.item_outline_color if not self.is_parent_or_self_hidden() else configuration.item_hidden_outline_color

    # ===========================================================================================
    # region Tree Traversal
    # ===========================================================================================

    def get_children(self):
        raise NotImplementedError()

    def is_parent_or_self_hidden(self):
        for item in self.get_parent_chain():
            if item.is_hidden:
                return True
        return False

    def _get_depth(self) -> int:
        return len(self.get_parent_chain())

    def get_parent_chain(self) -> list:
        chain = [self]
        while chain[-1].parent:
            chain.append(chain[-1].parent)
        chain.reverse()
        return chain

    def get_all_script_dependencies(self):
        raise NotImplementedError()

    def get_deepest_visible_in_parent_chain(self):
        chain = self.get_parent_chain()

        last_visible = chain[0]

        for item in chain[1:]:
            if last_visible.is_collapsed: break 
            if item.is_hidden: break
            last_visible = item

        if last_visible.is_hidden:  # None visible
            return None 

        return last_visible
    
    def is_child_of(self, other):
        return other in self.get_parent_chain()