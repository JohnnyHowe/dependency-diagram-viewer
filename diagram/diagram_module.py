from pygame import Rect, Vector2
import configuration
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramModule(DiagramItem):

    def __init__(self, path, name, center_position):
        super().__init__(path, name, center_position)
        self.folders = []
        self.scripts = []

    def draw(self):
        draw.rect(self.get_rect())
        draw.text(self.name, configuration.module_font_size, self.get_rect_with_padding())

        for child in self.folders + self.scripts:
            child.draw()

        self._expand_to_fit_children()

    def _expand_to_fit_children(self):
        self.rect = Rect(self.rect.center, (0, 0))
        for child in self.folders + self.scripts:
            self.rect = self.rect.union(child.rect)

        self.rect.topleft = Vector2(self.rect.topleft) - configuration.padding * Vector2(1, 1) - configuration.module_font_size * Vector2(0, 1) * 2
        self.rect.size = Vector2(self.rect.size) + (configuration.padding + configuration.module_font_size) * Vector2(1, 1) * 2