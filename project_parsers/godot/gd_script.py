from pathlib import Path
import re
from .project_script import ProjectScript


class GdScript(ProjectScript):
	def __init__(self, path):
		super().__init__(path)
		self._parse_file()

	def _parse_file(self):
		self._load_file_contents()
		self._set_class_name()

	def _load_file_contents(self):
		file = open(self.path, encoding="utf-8")
		self.file_contents = file.read()
		file.close()
		pattern = r"""(['"].*?['"]|#.*?$)"""
		self.file_contents_no_comments_or_strings = re.sub(pattern, '', self.file_contents, flags=re.MULTILINE)

	def _set_class_name(self):
		self._set_default_name()
		for line in self.file_contents.splitlines():
			line = line.strip()
			if not line.startswith("class_name "): continue
			self.name = line.split(" ", 1)[1]
			self.full_name = self.name
			return

	def _set_default_name(self):
		file_name = Path(self.path).parts[-1]
		self.name = file_name
		self.full_name = file_name

	def update_dependencies(self, all_scripts):
		dependencies = set()
		for script in all_scripts:
			if script == self:
				continue
			pattern = rf'\b{re.escape(script.name)}\b'
			if re.search(pattern, self.file_contents_no_comments_or_strings):
				dependencies.add(script)
		self.dependencies = list(dependencies)

	def __str__(self):
		return f"GdScript({self.name})"