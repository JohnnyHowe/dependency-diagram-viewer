from pygame import Vector2


class DiagramItem:

    def __init__(self, path: str, center_position: Vector2):
        self.path = path
        self.center_position = center_position
        self.hovered = False
        self.is_child_hovered = False

    def draw(self):
        pass