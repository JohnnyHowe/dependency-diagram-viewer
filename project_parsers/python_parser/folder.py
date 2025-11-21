import os
from pathlib import Path
from .script import Script


class Folder:
    def __init__(self, path, parent=None):
        self.path = path
        self.parent = parent
        self.folders = []
        self.scripts = []
        self._set_name()
        self._parse()
        if self.parent == None:
            self._set_dependencies()


    def _set_name(self):
        parts = Path(self.path).parts
        if len(parts) == 0:
            self.name = "[root]"
        else:
            self.name = parts[-1]

    def _parse(self):
        for child_name in os.listdir(self.path):
            self._parse_dir_child(child_name)

    def _parse_dir_child(self, child_name: str):
        if child_name.startswith("."): return
        if child_name.startswith("__"): return

        child_path = os.path.join(self.path, child_name)

        if os.path.isdir(child_path):
            self._parse_subfolder(child_path)
        elif child_path.endswith(".py"):
            self._parse_script(child_path)

    def _parse_subfolder(self, child_dir):
        folder = Folder(child_dir, self)
        if folder.has_scripts_recursive():
            self.folders.append(folder)

    def has_scripts_recursive(self):
        if len(self.scripts) > 0:
            return True

        for folder in self.folders:
            if folder.has_scripts_recursive():
                return True
            
        return False

    def _parse_script(self, child_dir):
        self.scripts.append(Script(child_dir, self))

    def as_dict(self) -> dict:
        return {
            "path": self.path,
            "full_name": self.path,
            "name": self.name,
            "scripts": [script.as_dict() for script in self.scripts],
            "folders": [folder.as_dict() for folder in self.folders]
        }
    
    def get_import_path_parts(self):
        if self.name == "[root]":
            return []
        if self.parent == None:
            return [self.name]
        return self.parent.get_import_path_parts() + [self.name]

    def get_all_scripts_recursive(self):
        all_scripts = list(self.scripts)
        for folder in self.folders:
            all_scripts += folder.get_all_scripts_recursive()
        return all_scripts

    def _set_dependencies(self):
        scripts = self.get_all_scripts_recursive()
        for script in scripts:
            script.set_dependencies(scripts)

