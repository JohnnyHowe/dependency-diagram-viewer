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
    
    def get_children(self):
        return []
 
    def get_all_script_dependencies(self):
        return self.dependencies

    def __str__(self):
        return f"DiagramScript({self.name})"

    def __repr__(self):
        return str(self)