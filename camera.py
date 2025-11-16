from singleton import Singleton
from pygame import Vector2, Rect

from window import Window


class Camera(metaclass=Singleton):
    position: Vector2
    zoom = 1

    def __init__(self):
        self.position = Vector2(0, 0)

    def project_rect(self, rect: Rect) -> Rect:
        return Rect(self.project_position(Vector2(rect.topleft)), self.project_size(Vector2(rect.size)))

    def project_position(self, position: Vector2) -> Vector2:
        return (position + Window().size / 2) * self.zoom - self.position

    def project_size(self, size: Vector2) -> Vector2:
        return size * self.zoom

    def project_size_component(self, size_component: float) -> float:
        return size_component * self.zoom