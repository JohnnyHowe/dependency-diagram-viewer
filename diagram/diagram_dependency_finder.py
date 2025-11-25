from diagram.dependency_display import DependencyDisplay


class DiagramDependencyFinder:
	def __init__(self, root):
		self.root = root

	def get_all_visible_dependency_pairs(self) -> list[DependencyDisplay]:
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
 