import os
from .gd_script import GdScript
from .project_folder import ProjectFolder
from .file_parser import *


class GdModule(ProjectFolder):
	def __init__(self, path):
		super().__init__(path)
		self._parse_project()

	def _parse_project(self):
		if not os.path.isdir(self.path):
			raise Exception("Path given is not folder! \"%s\"" % self.path)
		
		for folder_item_name in os.listdir(self.path):
			self._parse_folder_item(folder_item_name)
			
	def _parse_folder_item(self, path):
		folder_item_path = os.path.join(self.path, path)
		if ignore_path(folder_item_path):
			return

		if folder_item_path.endswith(".gd"):
			self._parse_gd_script(folder_item_path)
		if os.path.isdir(folder_item_path):
			self._parse_gd_module(folder_item_path)

	def _parse_gd_script(self, script_path):
		self.scripts.append(GdScript(script_path))

	def _parse_gd_module(self, module_path):
		submodule = GdModule(module_path)
		if submodule.contains_scripts_including_submodules():
			self.folders.append(submodule)

	def contains_scripts_including_submodules(self) -> bool:
		if len(self.scripts) > 0:
			return True
		for module in self.folders:
			if module.contains_scripts_including_submodules():
				return True
		return False

	def get_all_scripts_with_class_names(self):
		for script in self.get_all_scripts():
			if not script.name.endswith(".gd"):
				yield script

	def update_internal_dependencies(self):
		named_scripts = list(self.get_all_scripts_with_class_names())
		for script in self.get_all_scripts():
			script.update_dependencies(named_scripts)