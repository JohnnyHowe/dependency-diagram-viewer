from pathlib import Path


class ProjectFolder:
    def __init__(self, path):
        self.path = path
        self.full_name = path
        self._set_name()
        self.scripts = []
        self.folders = []

    def _set_name(self):
        parts = Path(self.path).parts
        if len(parts) <= 1:
            self.name = "[root]"
        else:
            self.name = parts[-1]

    def get_all_folders_recursive(self):
        folders = self.folders
        for folder in self.folders:
            folders += folder.get_all_folders_recursive()
        return folders

    def get_all_scripts(self):
        for script in self.scripts:
            yield script
        for folder in self.folders:
            for script in folder.get_all_scripts():
                yield script

    def get_all_dependency_pairs(self):
        """in form [(source, target), ...]"""
        for item in self.folders + self.scripts:
            for pair in item.get_all_dependency_pairs():
                yield pair

    def contains_path(self, path):
        return self.get_item_at_path(path) != None

    def get_item_at_path(self, path):
        if path == self.path:
            return self

        for script in self.scripts:
            if script.path == path:
                return script

        for folder in self.folders:
            found_item = folder.get_item_at_path(path)
            if found_item:
                return found_item
            
        return None

    def get_as_dict(self) -> dict:
        d = { "path": self.path, "folders": [], "scripts": [], "full_name": self.full_name, "name": self.name }
        for folder in self.folders:
            d["folders"].append(folder.get_as_dict())
        for script in self.scripts:
            d["scripts"].append(script.get_as_dict())
        return d