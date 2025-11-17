from pygame import Rect, Vector2
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramModule(DiagramItem):
    def __init__(self, path, center_position):
        super().__init__(path, center_position)
        self.folders = []
        self.scripts = []

    def draw(self):
        draw.rect(self.get_rect())
        for child in self.folders + self.scripts:
            child.draw()
        self._expand_to_fit_children()

    def _expand_to_fit_children(self):
        for child in self.folders + self.scripts:
            self.rect = self.rect.union(child.rect)