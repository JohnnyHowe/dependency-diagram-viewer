from pygame import Rect
import pygame

from diagram.diagram_loader import DiagramLoader
from window_engine.camera import Camera
import window_engine.draw as draw
from window_engine.window import Window
from camera_controller import CameraController

class DiagramViewer:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._camera_controller = CameraController()
        self._load_diagram()
        self.hovered_item = None
        self.held_item = None
        self._run()

    def _load_diagram(self):
        self.root = DiagramLoader(self.file_path).get_root()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._camera_controller.update()
        self._update_mouse_input()
        self._draw()
        Window().update()

    # ===========================================================================================
    # region Mouse
    # ===========================================================================================

    def _update_mouse_input(self):
        self._update_mouse_over()
        self._update_held_item()

    def _update_mouse_over(self):
        deepest_item_with_mouse_over = self._get_deepest_item_under_mouse()

        if self.hovered_item:
            self.hovered_item.is_hovered = False
        self.hovered_item = deepest_item_with_mouse_over
        if self.hovered_item:
            self.hovered_item.is_hovered = True

    def _get_deepest_item_under_mouse(self):
        deepest_item_with_mouse_over = None
        for item in self._get_items_under_mouse():
            if deepest_item_with_mouse_over == None:
                deepest_item_with_mouse_over = item
            elif item.depth > deepest_item_with_mouse_over.depth:
                deepest_item_with_mouse_over = item
        return deepest_item_with_mouse_over

    def _get_items_under_mouse(self):
        mouse_position = Camera().unproject_position(pygame.mouse.get_pos())
        for item in self.root.get_all_children_recursive():
            if item.is_root: continue
            if not item.rect.collidepoint(mouse_position): continue
            yield item
            
    def _update_held_item(self):
        if self.held_item:
            self.held_item.is_held = False
        self.held_item = None

        if self.hovered_item and pygame.mouse.get_pressed()[0]:
            self.held_item = self.hovered_item
            self.held_item.is_held = True

    # ===========================================================================================
    # region Drawing
    # ===========================================================================================

    def _draw(self):
        Window().surface.fill((0, 0, 0))
        self.root.draw()
        self._draw_controls_text()

    def _draw_controls_text(self):
        draw.text_screen_space("hold middle mouse to pan\nscrollwheel to zoom\n\nf: reset camera", 20, Rect((0, 0), Window().size))