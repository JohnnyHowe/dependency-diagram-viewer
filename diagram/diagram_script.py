from pygame import Rect, Vector2
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramScript(DiagramItem):
    size = Vector2(160, 40)
    font_size = 40

    def __init__(self, full_name, name, path, center_position):
        super().__init__(path, center_position)
        self.dependencies = []
        self.full_name = full_name
        self.name = name

    def draw(self):
        rect = self.get_rect()
        draw.rect(rect)
        draw.text(self.name, self.font_size, rect)

    def get_rect(self) -> Rect:
        rect = Rect(0, 0, 0, 0)
        rect.center = self.center_position
        rect.size = self.size
        return rect