import os
import json
import re


class Asmdef:
    guid: str

    def __init__(self, project_path, file_path_in_project):
        self.project_path = project_path
        self.file_path_in_project = file_path_in_project
        self.full_path = os.path.join(project_path, file_path_in_project)
        self.name = os.path.basename(self.file_path_in_project)

        self.guid_dependencies = []
        self.named_dependencies = []
        self.named_project_dependencies = []

        self._parse()

    def _parse(self):
        self._set_guid()
        with open(self.full_path, "r", encoding="utf-8-sig") as file:
            contents = file.read()
            self._asmdef_contents = json.loads(contents)

        for reference in self._asmdef_contents.get("references", []):
            if reference.startswith("GUID:"):
                self.guid_dependencies.append(reference[5:])
            else:
                self.named_dependencies.append(reference)

    def _set_guid(self):
        meta_path = self.full_path + ".meta"
        with open(meta_path, "r") as file:
            contents= file.read()
            match = re.search("guid: (.*)", contents)
            self.guid = match.group(1)

    def populate_named_dependencies(self, all_asmdefs):
        for asmdef in all_asmdefs:
            if asmdef == self:
                continue
            if asmdef.guid in self.guid_dependencies:
                self.named_dependencies.append(asmdef.name)

        self.named_project_dependencies = []
        for dependency in self.named_dependencies:
            if any(asmdef.name == dependency for asmdef in all_asmdefs):
                self.named_project_dependencies.append(dependency)

    def is_asmdef(file_path: str) -> bool:
        return file_path.endswith(".asmdef")

    def as_dict(self) -> dict:
        return {
            "path": str(self.file_path_in_project),
            "name": self.get_pretty_name(),
            "full_name": self.name,
            "dependencies": self.named_project_dependencies
        }

    def has_dependencies(self):
        return len(self.named_project_dependencies) > 0

    def get_pretty_name(self):
        return self.name[:-7]
        #parts = self.name[:-6].split(".")
        #if len(parts) == 1:
        #    return parts[0]
        #return ".".join(parts[:-1]) + ".\n" + parts[-1]

    def __str__(self):
        return f"Asmdef({self.name}, GUID: {self.guid})"

    def __repr__(self):
        return str(self)