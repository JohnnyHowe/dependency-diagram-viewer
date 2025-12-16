import os
from project_parsers.csharp_namespace_parser.json_parser import update_file
from project_parsers.csharp_namespace_parser.project import Project
from project_parsers.csharp_namespace_parser.namespace import Namespace


def write(file_path: str, project: Project):
    update_file(file_path, ProjectDictionaryConverter(project).get_as_dict())


def get_as_dict(project: Project) -> dict:
    return ProjectDictionaryConverter(project).get_as_dict()


class ProjectDictionaryConverter:
    def __init__(self, project: Project):
        self.project = project
        self._set_all_script_dependencies()

    def _set_all_script_dependencies(self):
        dependencies = {}

        for file_path in self.project.script_contents.keys():
            dependencies[file_path] = set()

        for member in self.project.get_members_recursive():
            member_dependencies = set(map(lambda member: member.file_path, member.member_dependencies))
            dependencies[member.file_path] = dependencies[member.file_path].union(member_dependencies).union(member.namespace_dependencies_not_in_members)

        self.all_script_dependencies = dependencies

    def get_as_dict(self) -> dict:

        hierarchy = {
            "path": self.project.path,
            "name": "",
            "folders": [],
            "scripts": []
        }

        for namespace_name in sorted(self.project.namespaces.keys()):
            self._add_namespace_to_hierarchy(hierarchy, self.project.namespaces[namespace_name])

        return hierarchy

    def _add_namespace_to_hierarchy(self, hierarchy: dict, namespace: Namespace):
        parts = namespace.get_full_namespace_parts()
        current_place_in_hierarchy = hierarchy
        for i in range(len(parts)):
            current_place_in_hierarchy = self._get_folder_by_name_create_if_necessary(current_place_in_hierarchy["folders"], ".".join(parts[:i + 1]))

        current_place_in_hierarchy["scripts"] = self._sorted_item_list(self._get_script_dicts(namespace))

    def _get_folder_by_name_create_if_necessary(self, folder_list: list, full_name: str):
        name = full_name.split(".")[-1]

        found = self._get_folder_by_name(folder_list, name)
        if found: return found
    
        new_folder = {
            "name": name,
            "path": full_name,
            "full_name": full_name,
            "folders": [],
            "scripts": []
        }
        folder_list.append(new_folder)
        return new_folder

    def _get_folder_by_name(self, folder_list: list, name: str):
        for folder in folder_list:
            if folder["name"] == name:
                return folder
        return None

    def _get_namespace_as_dict(self, namespace: Namespace):
        name = ''
        if len(namespace.name) > 0:
            name = namespace.name.split(".")[-1]

        return {
            "path": namespace.get_full_namespace(),
            "name": name,
            "scripts": self._sorted_item_list(list(self._get_script_dicts(namespace))),
            "folders": []
        }

    def _get_script_dicts(self, namespace: Namespace):
        for script_path in namespace.scripts:
            yield self._get_script_dict(namespace, script_path)

    def _get_script_dict(self, containing_namespace: Namespace, script_path: str) -> dict:
        file_name = os.path.basename(script_path)
        return {
            "name": file_name,
            "path": script_path,
            "full_name": script_path,
            "dependencies": sorted(list(self.all_script_dependencies[script_path]))
        }

    def _sorted_item_list(self, items: list) -> list:
        return sorted(items, key=lambda item: item["path"])
