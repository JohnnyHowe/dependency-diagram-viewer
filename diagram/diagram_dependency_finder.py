from typing import Generator
from diagram.dependency_display import DependencyDisplay
from diagram.diagram_item import DiagramItem


class DiagramDependencyFinder:
	def __init__(self, root):
		self.root = root

	def get_all_visible_dependencies(self) -> list[DependencyDisplay]:
		dependencies = []
		for dependency_source in self._get_visible_items(self.root.get_scripts_recursive()):
			dependencies += self._get_all_visible_dependencies_for_source(dependency_source)
		return dependencies

	def _get_all_visible_dependencies_for_source(self, source: DiagramItem) -> Generator[DependencyDisplay, None, None]:
		for target in source.get_all_script_dependencies():
			for dependency_display in self._get_dependency_displays(source, target):
				yield dependency_display

	def _get_dependency_displays(self, source: DiagramItem, target: DiagramItem) -> list[DependencyDisplay]:
		# take the deepest visible parent of target
		deepest_target_parent = target.get_deepest_visible_in_parent_chain()

		# Unless parent is parent of source - then nothing
		if source.is_child_of(deepest_target_parent):
			return []

		return [DependencyDisplay(source, deepest_target_parent)]

	def _get_visible_items(self, items_list):
		items = set()
		for item in items_list:
			deepest_item = item.get_deepest_visible_in_parent_chain()
			if deepest_item is None: continue
			items.add(deepest_item)
		return items
 