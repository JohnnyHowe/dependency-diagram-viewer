from pathlib import Path
import re
from .project_script import ProjectScript


class GdScript(ProjectScript):
	def __init__(self, path):
		super().__init__(path)
		self.name = Path(path).parts[-1]
		self.full_name = self.path
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
		self.class_name = None
		for line in self.file_contents.splitlines():
			line = line.strip()
			if not line.startswith("class_name "): continue
			self.class_name = line.split(" ", 1)[1]

	def update_dependencies(self, all_scripts):
		dependencies = set()
		for script in all_scripts:
			if script == self:
				continue
			pattern = rf'\b{re.escape(script.class_name)}\b'
			if re.search(pattern, self.file_contents_no_comments_or_strings):
				dependencies.add(script)
		self.dependencies = list(dependencies)

	def __str__(self):
		return f"GdScript({self.name})"