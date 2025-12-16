import os
from pathlib import Path

import json_parser
from .asmdef import Asmdef

class Parser:
    def __init__(self, project_path: str, output_path: str) -> None:
        self.project_path = Path(project_path)
        self.output_path = Path(output_path)
        self.asmdefs = {}
        self._parse()

        all_asmdefs = list(self.asmdefs.values())
        for asmdef in all_asmdefs:
            asmdef.populate_named_dependencies(all_asmdefs)

        self._cull_with_no_dependencies()

    def _parse(self):
        for root, dirs, files in os.walk(self.project_path):
            for file_name in files:
                if Asmdef.is_asmdef(file_name):
                    self._create_asmdef(Path(os.path.join(root, file_name)))

    def _cull_with_no_dependencies(self):
        known_names = set()
        for asmdef in self.asmdefs.values():
            if asmdef.has_dependencies():
                known_names = known_names.union(set(asmdef.named_project_dependencies))
                known_names.add(asmdef.name)

        asmdefs = {}
        for asmdef in self.asmdefs.values():
            if asmdef.name in known_names:
                asmdefs[asmdef.guid] = asmdef
            
        self.asmdefs = asmdefs

    def _create_asmdef(self, full_path: str):
        file_path_in_project = Path(str(full_path)[len(str(self.project_path)):].strip("/").strip("\\"))
        asmdef = Asmdef(self.project_path, file_path_in_project)
        self.asmdefs[asmdef.guid] = asmdef

    def as_dict(self) -> dict:
        return {
            "path": "",
            "name": "",
            "folders": [],
            "scripts": list([asmdef.as_dict() for asmdef in self.asmdefs.values()])
        }

    def update_dependencies_file(self):
        json_parser.update_file(self.output_path, self.as_dict())