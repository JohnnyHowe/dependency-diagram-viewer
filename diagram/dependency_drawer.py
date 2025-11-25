import configuration
from diagram.dependency_display import DependencyDisplay
from diagram.diagram_dependency_finder import DiagramDependencyFinder
from diagram.diagram_module import DiagramModule
from window_engine import draw


class DependencyDrawer:
	diagram_dependency_finder: DiagramDependencyFinder
	root: DiagramModule
	selected_items: set

	def draw_dependencies(self, root: DiagramModule, selected_items: set):
		self.root = root
		self.selected_items = selected_items
		self.diagram_dependency_finder = DiagramDependencyFinder(root)

		pairs = set(self.diagram_dependency_finder.get_all_visible_dependency_pairs())
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
