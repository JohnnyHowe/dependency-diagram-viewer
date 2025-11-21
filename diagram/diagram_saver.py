import json
from diagram.diagram_item import DiagramItem
from diagram.diagram_module import DiagramModule
from diagram.diagram_script import DiagramScript


class DiagramSaver:
    def __init__(self, file_path: str, root: DiagramModule):
        self.file_path = file_path
        self.root = root

    def save(self):
        d = self._get_module_as_dict(self.root)
        json_str = json.dumps(d, indent=4)
        with open(self.file_path, "w") as file:
            file.write(json_str)

    def _get_module_as_dict(self, module: DiagramModule) -> dict:
        d = self._get_item_as_dict(module)
        d["is_collapsed"] = module.is_collapsed

        d["folders"] = []
        for submodule in module.modules:
            d["folders"].append(self._get_module_as_dict(submodule))
        d["folders"] = sorted(d["folders"], key = lambda item: item["name"])

        scripts = []
        for submodule in module.scripts:
            scripts.append(self._get_script_as_dict(submodule))
        d["scripts"] = sorted(scripts, key = lambda item: item["name"])


        return d

    def _get_script_as_dict(self, item) -> dict:
        d = self._get_item_as_dict(item)
        d["full_name"] = item.full_name
        d["dependencies"] = []
        d["position"] = item.rect.center
        for dependency in item.dependencies:
            if isinstance(dependency, DiagramScript):
                d["dependencies"].append(dependency.full_name)
            else:
                d["dependencies"].append(dependency.path)
        return d

    def _get_item_as_dict(self, item: DiagramItem) -> dict:
        return {
            "path": item.path,
            "name": item.name,
            "is_hidden": item.is_hidden,
        }