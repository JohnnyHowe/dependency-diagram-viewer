from typing import Generator
from diagram.dependency_display import DependencyDisplay
from diagram.diagram_item import DiagramItem


class DiagramDependencyFinder:
	def __init__(self, root):
		self.root = root

	def get_all_visible_dependencies(self) -> list[DependencyDisplay]:
		self._set_all_dependencies()
		self._raise_dependencies_to_visible_parents()
		self._filter_self_dependencies()
		self._filter_duplicates()
		self._filter()
		self._filter_mutual_dependencies()
		self.dependencies = sorted(list(self.dependencies))
		return self.dependencies

	def _set_all_dependencies(self):
		self.dependencies = set()
		for source in self.root.get_scripts_recursive():
			for target in source.get_all_script_dependencies():
				self.dependencies.add(DependencyDisplay(source, target))

	def _raise_dependencies_to_visible_parents(self):
		raised = set()
		for dependency in self.dependencies:
			raised.add(DependencyDisplay(
				dependency.source.get_deepest_visible_in_parent_chain(),
				dependency.target.get_deepest_visible_in_parent_chain(),
			))
		self.dependencies = raised

	def _filter_duplicates(self):
		filtered = set()
		seen = set()
		for dependency in self.dependencies:
			if dependency.pair in seen: continue
			seen.add(dependency.pair)
			filtered.add(dependency)
		self.dependencies = filtered

	def _filter_self_dependencies(self):
		filtered = set()
		for dependency in self.dependencies:
			if not dependency.source == dependency.target:
				filtered.add(dependency)
		self.dependencies = filtered

	def _filter(self):
		filtered = set()
		for dependency in self.dependencies:

			if dependency.source.is_root or dependency.target.is_root:
				continue
			if dependency.source.is_child_of(dependency.target) or dependency.target.is_child_of(dependency.source):
				continue

			filtered.add(dependency)

		self.dependencies = filtered
 
	def _filter_mutual_dependencies(self):
		dependencies_by_pair = {}

		for dependency in self.dependencies:
			if dependency.inverse_pair in dependencies_by_pair:
				dependencies_by_pair[dependency.inverse_pair].dependency_type = "mutual"
			else:
				dependencies_by_pair[dependency.pair] = dependency

		self.dependencies = set(dependencies_by_pair.values())