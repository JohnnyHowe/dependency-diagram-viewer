from pygame import Vector2
from singleton import Singleton


class Camera(metaclass=Singleton):
    position: Vector2

    def __init__(self):
        self.position = Vector2(0, 0)