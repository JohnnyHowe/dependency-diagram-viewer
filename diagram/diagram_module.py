from pygame import Rect, Vector2
import configuration
from diagram.diagram_item import DiagramItem
from window_engine import draw


class DiagramModule(DiagramItem):
    min_size = Vector2(160, 80)

    def __init__(self, path, name, parent, center_position):
        super().__init__(path, name, parent, center_position)
        self.folders = []
        self.scripts = []
        self.is_collapsed = False

    def draw(self):
        if not self.is_root:
            self._draw_shape()
            text = self.name + (" +" if self.is_collapsed else "")
            draw.text(text, configuration.module_font_size, self.get_rect_with_padding(), self.get_outline_color())

        if not self.is_collapsed:
            for child in self.folders + self.scripts:
                child.draw()

    def update(self):
        self._update_size()
        for submodule in self.folders:
            submodule.update()

    def _draw_shape(self):
        self.draw_background_fill()
        draw.rect(self.rect, self.get_outline_color())

        detail_size = configuration.module_detail_size

        detail = Rect(Vector2(self.rect.topleft) + Vector2(-1, 1) * detail_size, Vector2(detail_size * 2, detail_size))
        draw.rect(detail, self.get_outline_color())
        detail.topleft = Vector2(detail.topleft) + Vector2(0, 1) * detail_size * 2
        draw.rect(detail, self.get_outline_color())

    def _update_size(self):
        self._expand_to_fit_children()

        if self._is_self_or_parent_collapsed():
            center = self.rect.center
            self.rect = Rect((0, 0), self.min_size)
            self.rect.center = center

    def _is_self_or_parent_collapsed(self):
        for item in self.get_parent_chain():
            if item.is_collapsed:
                return True
        return False

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

    def get_all_visible_children_recursive(self):
        if self.is_collapsed:
            return [self]
        children = [self, ] + self.scripts
        for folder in self.folders:
            children += folder.get_all_visible_children_recursive()
        return children

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