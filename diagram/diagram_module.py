from pygame import Rect, Vector2
import configuration
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramModule(DiagramItem):

    def __init__(self, path, name, parent, center_position):
        super().__init__(path, name, parent, center_position)
        self.folders = []
        self.scripts = []

    def draw(self):
        if not self.is_root:
            self._draw_shape()
            draw.text(self.name, configuration.module_font_size, self.get_rect_with_padding())

        for child in self.folders + self.scripts:
            child.draw()

        self._expand_to_fit_children()

    def _draw_shape(self):
        self.draw_background_fill()
        draw.rect(self.rect)

        detail_size = configuration.module_detail_size

        detail = Rect(Vector2(self.rect.topleft) + Vector2(-1, 1) * detail_size, Vector2(detail_size * 2, detail_size))
        draw.rect(detail)
        detail.topleft = Vector2(detail.topleft) + Vector2(0, 1) * detail_size * 2
        draw.rect(detail)

    def _expand_to_fit_children(self):
        self.rect = Rect(self.rect.center, (0, 0))
        for child in self.folders + self.scripts:
            self.rect = self.rect.union(child.rect)

        header_padding = Vector2(0, configuration.module_font_size) * 2
        detail_padding = Vector2(configuration.module_detail_size, 0)
        padding = Vector2(1, 1) * configuration.padding

        self.rect.topleft = Vector2(self.rect.topleft) - (header_padding + detail_padding + padding)
        self.rect.size = Vector2(self.rect.size) + padding * 2 + detail_padding + header_padding

    def get_rect_with_padding(self):
        rect = Rect(self.rect) 

        detail_padding = Vector2(configuration.module_detail_size, 0)
        padding = Vector2(1, 1) * configuration.padding

        rect.topleft = Vector2(rect.topleft) + detail_padding + padding
        rect.size = Vector2(rect.size) - (padding * 2 + detail_padding)
        return rect

    def get_all_children_recursive(self):
        return self.get_scripts_recursive() + self.get_folders_recursive()

    def get_scripts_recursive(self):
        scripts = []
        for folder in self.get_folders_recursive():
            scripts += folder.scripts
        return scripts

    def get_folders_recursive(self):
        folders = [self] 
        for folder in self.folders:
            folders += folder.get_folders_recursive()
        return folders

    def move(self, change: Vector2):
        for child in self.folders + self.scripts:
            child.move(change)