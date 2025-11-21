from pathlib import Path

from .script_parser import *


class Script:
    def __init__(self, path, parent):
        self.path = path
        self.parent = parent
        self.name = Path(self.path).parts[-1]
        self._parse()

    def _parse(self):
        with open(self.path, "r") as file:
            self.contents = file.read()
        self.import_path = self.get_import_path()
        self.imports = get_imports(self.contents)

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "full_name": self.path,
            "name": self.name,
            "dependencies": [script.path for script in self.dependencies]
        }

    def get_import_path(self):
        return ".".join(self.get_import_path_parts())

    def get_import_path_parts(self):
        return self.parent.get_import_path_parts() + [self.name[:-3]]

    def set_dependencies(self, all_scripts):
        self.dependencies = []
        for script in all_scripts:
            if self._depends_on_script(script):
                self.dependencies.append(script)

    def _depends_on_script(self, script) -> bool:
        for full_import_path in self.imports:
            if is_import_path_match(script.import_path, full_import_path):
                return True
        return False