from pygame import Rect, Vector2
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramModule(DiagramItem):
    min_size = Vector2(160, 40)

    def __init__(self, path, center_position):
        super().__init__(path, center_position)
        self.folders = []
        self.scripts = []

    def draw(self):
        draw.rect(self.get_rect())
        for child in self.folders + self.scripts:
            child.draw()


    def get_rect(self) -> Rect:
        rect = Rect(0, 0, 0, 0)
        rect.center = self.center_position
        rect.size = self.min_size
        return rect