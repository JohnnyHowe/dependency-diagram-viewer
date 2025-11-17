import json

from pygame import Vector2

from diagram.diagram_module import DiagramModule
from diagram.diagram_script import DiagramScript

class DiagramLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._all_scripts = {}
        self._load()

    def _load(self):
        self._load_json()
        self._root = self._create_module_from_data_dict_recursive(None, self._raw_json)
        self._populate_all_script_dependencies()

    def _load_json(self):
        with open(self.file_path, "r") as file:
            self._raw_json = json.loads(file.read())

    def _create_module_from_data_dict_recursive(self, parent, data: dict) -> DiagramModule:
        module = DiagramModule(data["path"], data["name"], parent, data.get("position", Vector2(0, 0)))

        for script_data in data["scripts"]:
            module.scripts.append(self._create_script_from_data_dict(parent, script_data))

        for module_data in data["folders"]:
            module.scripts.append(self._create_module_from_data_dict_recursive(parent, module_data))

        return module

    def _create_script_from_data_dict(self, parent, data: dict) -> DiagramScript:
        script = DiagramScript(data["full_name"], data["name"], data["path"], parent, data.get("position", Vector2(0, 0)))
        self._all_scripts[script.full_name] = [script, data]
        return script

    def _populate_all_script_dependencies(self):
        for script, json_data in self._all_scripts.values():
            self._populate_script_dependencies(script, json_data)

    def _populate_script_dependencies(self, script: DiagramScript, json_data: dict):
        script.dependencies = []
        dependency_names = json_data["dependencies"]
        for dependency_full_name in dependency_names:
            script.dependencies.append(self._all_scripts[dependency_full_name])

    def get_root(self):
        return self._root
