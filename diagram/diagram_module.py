from pygame import Rect, Vector2
import configuration
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
        self.rect = Rect(self.rect.center, (0, 0))
        for child in self.folders + self.scripts:
            self.rect = self.rect.union(child.rect)

        padding_vec = Vector2(configuration.padding, configuration.padding)
        self.rect.topleft = Vector2(self.rect.topleft) - padding_vec
        self.rect.size += padding_vec * 2