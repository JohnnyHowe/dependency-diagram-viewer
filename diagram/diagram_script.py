from pygame import Rect, Vector2
import configuration
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramScript(DiagramItem):
    def __init__(self, full_name, name, path, parent, center_position):
        super().__init__(path, name, parent, center_position)
        self.dependencies = []
        self.full_name = full_name
        self.name = name

    def draw(self):
        rect = self.rect
        self.draw_background_fill()
        draw.rect(rect)
        draw.text(self.name, configuration.script_font_size, self.get_rect_with_padding(), h_alignment=0, v_alignment=0)