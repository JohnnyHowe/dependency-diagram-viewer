from typing import Generator
from diagram.dependency_display import DependencyDisplay
from diagram.diagram_item import DiagramItem


class DiagramDependencyFinder:
	def __init__(self, root):
		self.root = root

	def get_all_visible_dependencies(self) -> list[DependencyDisplay]:
		self.dependencies = []
		for dependency_source in self._get_visible_items(self.root.get_scripts_recursive()):
			self._get_all_visible_dependencies_for_source(dependency_source)
		self._filter_mutual_dependencies()
		return self.dependencies

	def _get_all_visible_dependencies_for_source(self, source: DiagramItem):
		for target in source.get_all_script_dependencies():
			self._get_dependency_displays(source, target)

	def _get_dependency_displays(self, source: DiagramItem, target: DiagramItem):
		# take the deepest visible parent of target
		deepest_target_parent = target.get_deepest_visible_in_parent_chain()

		# Unless parent is parent of source - then nothing
		if source.is_child_of(deepest_target_parent):
			return

		direct = deepest_target_parent == target
		dependency_type = "direct" if direct else None
		self.dependencies.append(DependencyDisplay(source, deepest_target_parent, dependency_type))

	def _get_visible_items(self, items_list):
		items = set()
		for item in items_list:
			deepest_item = item.get_deepest_visible_in_parent_chain()
			if deepest_item is None: continue
			items.add(deepest_item)
		return items
 
	def _filter_mutual_dependencies(self):
		to_remove = []

		# find ones to remove
		seen_pairs = {}
		for dependency in self.dependencies:
			if dependency.inverse_pair in seen_pairs:
				to_remove.append(dependency)
			seen_pairs[dependency.pair] = dependency

		# remove
		for dependency in to_remove:
			self.dependencies.remove(dependency)

		# update non-removed one to "mutual"
		for dependency in to_remove:
			seen_pairs[dependency.inverse_pair].dependency_type = "mutual"