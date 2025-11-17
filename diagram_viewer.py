from pygame import Rect

from diagram.diagram_loader import DiagramLoader
import window_engine.draw as draw
from window_engine.window import Window
from camera_controller import CameraController

class DiagramViewer:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._camera_controller = CameraController()
        self._load_diagram()
        self._run()

    def _load_diagram(self):
        self.root = DiagramLoader(self.file_path).get_root()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._camera_controller.update()
        self._update_mouse_over()
        self._draw()
        Window().update()

    def _update_mouse_over(self):
        deepest_item_with_mouse_over = None
        deepest_item_with_mouse_over_depth = None

    def _draw(self):
        Window().surface.fill((0, 0, 0))
        self.root.draw()
        self._draw_controls_text()

    def _draw_controls_text(self):
        draw.text_screen_space("hold middle mouse to pan\nscrollwheel to zoom\n\nf: reset camera", 20, Rect((0, 0), Window().size))