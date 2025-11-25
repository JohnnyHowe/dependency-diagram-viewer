from pygame import Rect, Vector2
import pygame

import configuration
from dependency_display import DependencyDisplay
from diagram.diagram_loader import DiagramLoader
from diagram.diagram_module import DiagramModule
from diagram.diagram_saver import DiagramSaver
import window_engine.draw as draw
from window_engine.mouse import Mouse
from window_engine.window import Window
from camera_controller import CameraController

class DiagramViewer:
	selection_mouse_button_index = 1

	def __init__(self, parser):
		self.parser = parser
		self.reload_diagram()

		self._camera_controller = CameraController()

		self.running = True
		self.hovered_item = None
		self.selected_items = set()
		self.is_holding_selection = False
		self.selection_start_position = None

		self.space_children = False
		self.reset_callback = None

		self._run()

	def reload_diagram(self):
		self.parser.update_dependencies_file()
		self.root = DiagramLoader(self.parser.output_path).get_root()

	def _run(self):
		while self.running:
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
			DiagramSaver(self.parser.output_path, self.root).save()
		if key == pygame.K_a:
			self.space_children = not self.space_children
		if key == pygame.K_r:
			Window().queue_draw_call(lambda: Window().surface.fill("#000000"), 10)
			draw.text_screen_space("Reloading...", 20, Rect((0, 0), Window().size), layer=11, v_alignment=0, h_alignment=0)
			Window().update()
			self.parser.update_dependencies_file()
			self.reload_diagram()

	def _toggle_selection_visibility(self):
		balance = 0
		for item in self.selected_items:
			balance += -1 if item.is_hidden else 1
		new_state = balance >= 0
		for item in self.selected_items:
			item.is_hidden = new_state 

	def _toggle_selection_collapse(self):
		modules = []
		for item in self.selected_items:
			if isinstance(item, DiagramModule):
				modules.append(item)
		balance = 0
		for item in modules:
			balance += -1 if item.is_collapsed else 1
		new_state = balance >= 0
		for item in modules:
			item.is_collapsed = new_state

	def _reset_positions(self):
		for child in self.root.get_all_children_recursive():
			child.rect.center = Vector2(0, 0)

	# ===========================================================================================
	# region Mouse Input/Selection
	# ===========================================================================================

	def _update_mouse_input(self):
		self._update_hover()
		self._move_held_items()

		for event in Window().pygame_events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self._mouse_down(event.button)
			if event.type == pygame.MOUSEBUTTONUP:
				self._mouse_up(event.button)

	def _update_hover(self):
		if self.is_holding_selection: return
		deepest_item_with_mouse_over = self._get_deepest_visible_item_under_mouse()

		if self.hovered_item:
			self.hovered_item.is_hovered = False
		self.hovered_item = deepest_item_with_mouse_over
		if self.hovered_item:
			self.hovered_item.is_hovered = True

	def _get_deepest_visible_item_under_mouse(self):
		deepest_item_with_mouse_over = None
		for item in self._get_visible_items_under_mouse():
			if deepest_item_with_mouse_over == None:
				deepest_item_with_mouse_over = item
			elif item.depth > deepest_item_with_mouse_over.depth:
				deepest_item_with_mouse_over = item
		return deepest_item_with_mouse_over

	def _get_visible_items_under_mouse(self):
		for item in self.root.get_all_visible_children_recursive():
			if item.is_root: continue
			if not item.rect.collidepoint(Mouse().position): continue
			yield item

	def _mouse_down(self, button_index: int):
		if button_index != self.selection_mouse_button_index: return
		self.is_holding_selection = self._is_mouse_over_selected_item()
		self.selection_start_position = Mouse().position

	def _is_mouse_over_selected_item(self) -> bool:
		mouse_pos = Mouse().position
		for item in self.selected_items:
			if item.rect.collidepoint(mouse_pos) and not self._is_mouse_over_visible_child(item):
				return True
		return False

	def _is_mouse_over_visible_child(self, item):
		mouse_pos = Mouse().position
		if isinstance(item, DiagramModule):
			if item.is_collapsed:
				return False
		for child in item.get_children():
			if child.rect.collidepoint(mouse_pos):
				return True
		return False

	def _mouse_up(self, button_index: int):
		if button_index != self.selection_mouse_button_index: return

		if self.is_holding_selection:
			if pygame.key.get_pressed()[pygame.K_LCTRL]:
				self._toggle_selected(set(self._get_items_to_select()))
			else:
				self.is_holding_selection = False
				if Mouse().position == self.selection_start_position:
					self._set_selection()
		else:
			if pygame.key.get_pressed()[pygame.K_LCTRL]:
				self._toggle_selected(set(self._get_items_to_select()))
			else:
				self._set_selection()

		self.selection_start_position = None
		self.is_holding_selection = False

	def _toggle_selected(self, items: set):
		held_score = sum([1 if item in self.selected_items else -1 for item in items])
		new_state = held_score < 0

		for item in items:
			item.is_held = new_state

		if new_state:
			self.selected_items = self.selected_items.union(items)
		else:
			self.selected_items -= items 

	def _set_selection(self):
		if not pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_LCTRL]:
			self._clear_selection()

		self.selected_items = self.selected_items.union(self._get_items_to_select())
		for item in self.selected_items:
			item.is_held = True

	def _get_items_to_select(self):
		items_to_select = self._get_outermost_visible_items_contained_in_selection_rect()
		if len(items_to_select) == 0:
			item_under_mouse = self._get_deepest_visible_item_under_mouse()
			if item_under_mouse:
				items_to_select = [item_under_mouse]
		return items_to_select

	def _get_outermost_visible_items_contained_in_selection_rect(self):
		items = set()
		for item in sorted(self._get_visible_items_contained_in_selection_rect(), key=lambda item: item.depth):

			already_in = False
			for parent in item.get_parent_chain():
				if parent in items:
					already_in = True
					continue

			if not already_in:
				items.add(item)

		return items

	def _get_visible_items_contained_in_selection_rect(self):
		rect = self._get_selection_rect()
		for item in self.root.get_all_visible_children_recursive():
			if rect.contains(item.rect):
				yield item

	def _clear_selection(self):
		for item in self.selected_items:
			item.is_held = False
		self.selected_items = set()

	def _get_selection_rect(self):
		if self.selection_start_position is None:
			return None
		current_pos = Mouse().position
		rect = Rect(current_pos, self.selection_start_position - current_pos)
		rect.normalize()
		return rect

	def _move_held_items(self):
		if not self.is_holding_selection: return
		rel = Mouse().rel
		for item in self.selected_items:
			item.move(rel)

	# ===========================================================================================
	# region Drawing
	# ===========================================================================================

	def _draw(self):
		Window().surface.fill((0, 0, 0))
		self.root.draw()
		self._draw_dependencies()
		self._draw_selection()
		self._draw_controls_text()

	def _draw_selection(self):
		self._draw_selection_rect()

	def _draw_selection_rect(self):
		if self.selection_start_position is None or self.is_holding_selection:
			return
		draw.rect(self._get_selection_rect(), "#0000ff")

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
			"",
			"s: save"
			"r: reload/parse project again",
		]
		draw.text_screen_space("\n".join(lines), 20, Rect((0, 0), Window().size))

	def _draw_dependencies(self):
		pairs = set(self._get_all_visible_dependency_pairs())
		seen = set()

		for dependency_display in pairs:
			if dependency_display.pair in seen: continue
			focussed = len(self.selected_items) == 0 or self._is_dependency_targetted(dependency_display)

			if dependency_display.inverse_pair in pairs:
				self._draw_mutual_dependency(dependency_display)
			else:
				draw.arrow(dependency_display.source.rect.midtop, dependency_display.target.rect.midbottom, self._get_dependency_color(dependency_display), layer=1 if focussed else 0)

			seen.add(dependency_display.pair)
			seen.add(dependency_display.inverse_pair)

	def _draw_mutual_dependency(self, pair):
		left = pair[0] if pair[0].rect.center[0] < pair[1].rect.center[0] else pair[1]
		right = pair[0] if left == pair[1] else pair[1]
		focussed = len(self.selected_items) == 0 or self._is_dependency_targetted(pair)
		color = configuration.dependency_wrong_way_color if focussed else configuration.dependency_wrong_way_unfocussed_color
		draw.arrow(right.rect.midleft, left.rect.midright, color, layer=2)
		draw.arrow(left.rect.midright, right.rect.midleft, color, layer=2)

	def _get_dependency_color(self, dependency_display: DependencyDisplay):
		focussed = len(self.selected_items) == 0 or self._is_dependency_targetted(dependency_display)
		wrong_way = dependency_display.source.rect.midtop[1] < dependency_display.target.rect.midbottom[1]
		if focussed:
			color = configuration.dependency_wrong_way_color if wrong_way else configuration.dependency_default_color
		else:
			color = configuration.dependency_wrong_way_unfocussed_color if wrong_way else configuration.dependency_unfocussed_color
		return color

	def _is_dependency_targetted(self, dependency_display: DependencyDisplay):
		for item in dependency_display.pair:
			for parent in item.get_parent_chain():
				if parent in self.selected_items:
					return True
		return False

	def _get_all_visible_dependency_pairs(self) -> list[DependencyDisplay]:
		pairs = []
		for dependency_source in self._get_visible_items(self.root.get_scripts_recursive()):
			for dependency_target in self._get_visible_items(dependency_source.get_all_script_dependencies()):
				if dependency_source == dependency_target: continue
				pairs.append(DependencyDisplay(dependency_source, dependency_target))
		return pairs

	def _get_visible_items(self, items_list):
		items = set()
		for item in items_list:
			deepest_item = item.get_deepest_visible_in_parent_chain()
			if deepest_item is None: continue
			items.add(deepest_item)
		return items
 