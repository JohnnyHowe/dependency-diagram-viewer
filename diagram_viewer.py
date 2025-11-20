from pygame import Rect, Vector2
import pygame

from diagram.diagram_loader import DiagramLoader
from diagram.diagram_module import DiagramModule
from diagram.diagram_saver import DiagramSaver
import window_engine.draw as draw
from window_engine.mouse import Mouse
from window_engine.window import Window
from camera_controller import CameraController

class DiagramViewer:
    file_path: str
    selection_mouse_button_index = 1

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._camera_controller = CameraController()
        self._load_diagram()
        self.hovered_item = None
        self.held_item = None
        self.space_children = False
        self._run()

    def _load_diagram(self):
        self.root = DiagramLoader(self.file_path).get_root()

    def _run(self):
        while True:
            self._run_frame()

    def _run_frame(self):
        self._camera_controller.update()
        Mouse().update()

        self._update_mouse_input()
        self._update_key_input()

        self.root.update()
        if self.space_children:
            self.root.space_children()

        self._draw()
        Window().update()

    # ===========================================================================================
    # region Key input
    # ===========================================================================================

    def _update_key_input(self):
        for event in Window().pygame_events:
            if event.type == pygame.KEYDOWN:
                self._keydown(event.key)

    def _keydown(self, key: int):
        if key == pygame.K_h:
            self._toggle_selection_visibility()
        if key == pygame.K_c:
            self._toggle_selection_collapse()
        if key == pygame.K_s:
            DiagramSaver(self.file_path, self.root).save()
        if key == pygame.K_a:
            self.space_children = not self.space_children
        if key == pygame.K_r:
            self._reset_positions()

    def _toggle_selection_visibility(self):
        if self.held_item:
            self.held_item.is_hidden = not self.held_item.is_hidden

    def _toggle_selection_collapse(self):
        if isinstance(self.held_item, DiagramModule):
            self.held_item.is_collapsed = not self.held_item.is_collapsed

    def _reset_positions(self):
        for child in self.root.get_all_children_recursive():
            child.rect.center = Vector2(0, 0)

    # ===========================================================================================
    # region Mouse input
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
        for item in self.root.get_all_visible_children_recursive():
            if item.is_root: continue
            if not item.rect.collidepoint(Mouse().position): continue
            yield item
            
    def _update_held_item(self):
        for event in Window().pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_down(event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                self._mouse_up(event.button)

        self._move_held_item()

    def _mouse_down(self, button_index: int):
        if button_index != self.selection_mouse_button_index: return

        if self.hovered_item:
            self.held_item = self.hovered_item
            self.held_item.is_held = True

    def _mouse_up(self, button_index: int):
        if button_index != self.selection_mouse_button_index: return

        if self.held_item:
            self.held_item.is_held = False
            self.held_item = None

    def _move_held_item(self):
        if self.held_item:
            self.held_item.move(Mouse().rel)

    # ===========================================================================================
    # region Drawing
    # ===========================================================================================

    def _draw(self):
        Window().surface.fill((0, 0, 0))
        self.root.draw()
        self._draw_dependencies()
        self._draw_controls_text()

    def _draw_controls_text(self):
        lines = [
            "hold middle mouse to pan", 
            "hold left mouse to select and move items",
            "scrollwheel to zoom",
            "",
            "f: reset camera",
            "h: toggle visibility on selection",
            "c: collapse/expand selection",
            "a: turn %s auto spacing" % ("off" if self.space_children else "on"),
            "r: reset all positions",
            "",
            "s: save"
        ]
        draw.text_screen_space("\n".join(lines), 20, Rect((0, 0), Window().size))

    def _draw_dependencies(self):
        pairs = self._get_all_visible_dependency_pairs()

        selected_pairs = []
        other_pairs = []
        for pair in pairs:
            if self._is_dependency_targetted(pair): 
                selected_pairs.append(pair)
            else:
                other_pairs.append(pair)

        is_item_targetted = self.held_item != None or self.hovered_item != None

        other_color = "#444444" if is_item_targetted > 0 else "#ffffff"
        other_layer = -1 if is_item_targetted > 0 else 1
        for pair in other_pairs:
            draw.arrow(pair[0].rect.midtop, pair[1].rect.midbottom, other_color, 4, other_layer)

        for pair in selected_pairs:
            draw.arrow(pair[0].rect.midtop, pair[1].rect.midbottom, "#ff0000", 4, 2)

    def _is_dependency_targetted(self, pair):
        targetted_item = self.held_item if self.held_item else self.hovered_item
        return targetted_item in pair[0].get_parent_chain() or targetted_item in pair[1].get_parent_chain()

    def _get_all_visible_dependency_pairs(self) -> list[tuple]:
        pairs = []
        for dependency_source in self._get_visible_items(self.root.get_scripts_recursive()):
            for dependency_target in self._get_visible_items(dependency_source.get_all_script_dependencies()):
                if dependency_source == dependency_target: continue
                pairs.append((dependency_source, dependency_target))
        return pairs

    def _get_visible_items(self, items_list):
        items = set()
        for item in items_list:
            deepest_item = item.get_deepest_visible_in_parent_chain()
            if deepest_item is None: continue
            items.add(deepest_item)
        return items
 