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

		for dependency_display in self.diagram_dependency_finder.get_all_visible_dependencies():
			self._draw_dependency(dependency_display)

	def _draw_dependency(self, dependency: DependencyDisplay) -> None:
		focussed = len(self.selected_items) == 0 or self._is_dependency_targetted(dependency)
		draw.arrow(dependency.get_start_position(), dependency.get_end_position(), self._get_dependency_color(dependency), layer=1 if focussed else 0)

	def _get_dependency_color(self, dependency_display: DependencyDisplay):
		focussed = len(self.selected_items) == 0 or self._is_dependency_targetted(dependency_display)
		wrong_way = dependency_display.source.rect.midtop[1] < dependency_display.target.rect.midbottom[1] or dependency_display.dependency_type == "mutual"
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
