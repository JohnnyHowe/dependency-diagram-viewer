from pygame import Rect, Vector2
import configuration
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramScript(DiagramItem):
    def __init__(self, full_name, name, path, parent, center_position):
        super().__init__(path, name, parent)
        self.dependencies = []
        self.full_name = full_name
        self.rect.center = center_position

    def draw(self):
        rect = self.rect
        self.draw_background_fill()
        draw.rect(rect, self.get_outline_color())
        draw.text(self.name, configuration.script_font_size, self.get_rect_with_padding(), h_alignment=0, v_alignment=0, color=self.get_outline_color())

    def get_deepest_visible_in_parent_chain(self):
        chain = self.get_parent_chain()
        last_visible = chain[0]

        for item in chain[1:]:
            if last_visible.is_collapsed: break 
            if last_visible.is_hidden: break 
            last_visible = item

        return last_visible