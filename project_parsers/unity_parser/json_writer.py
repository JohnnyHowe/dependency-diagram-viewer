from argparse import Namespace
import re

from project_parsers.unity_parser.json_parser import update_file
from project_parsers.unity_parser.project import Project


def write(file_path: str, project: Project):
    d = _get_as_dict(project)
    update_file(file_path, d)


def _get_as_dict(project: Project) -> dict:

    namespaces_to_contained_files = {}
    for namespace in project.namespaces.values():
        namespaces_to_contained_files[namespace.name] = set(_get_files_in_namespace(namespace))

    script_dependencies = _get_script_dependencies(project)
    grouped_namespaces = _get_grouped_namespaces(project.namespaces.keys())

    return _create_data_dict(project, "", grouped_namespaces, namespaces_to_contained_files, script_dependencies)


def _create_data_dict(project: Project, current_namespace: str, grouped_namespaces: dict, namespaces_to_contained_files, script_dependencies) -> dict:
    d = {
        "path": current_namespace,
        "full_name": current_namespace,
        "name": current_namespace.split(".")[-1],
        "folders": [],
        "scripts": [],
    }

    if current_namespace in namespaces_to_contained_files:
        for file_path in namespaces_to_contained_files[current_namespace]:
            d["scripts"].append({
                "path": file_path, 
                "full_name": file_path,
                "name": re.split(r"[\\/]", file_path)[-1],
                "dependencies": sorted(list(script_dependencies[file_path]))
            })

    for namespace_base, namespace_children in grouped_namespaces.items():
        name = ".".join([current_namespace, namespace_base]).strip(".")
        data_dict = _create_data_dict(project, name, namespace_children, namespaces_to_contained_files, script_dependencies)
        if namespace_base == "none":
            d["scripts"] = data_dict["scripts"]
        else:
            d["folders"].append(data_dict)

    d["scripts"] = sorted(d["scripts"], key=lambda item: item["path"])
    d["folders"] = sorted(d["folders"], key=lambda item: item["path"])
    return d


def _get_grouped_namespaces(all_namespaces):
    grouped = {}
    for namespace in all_namespaces:
        _add_namespace_to_grouping(grouped, namespace.split("."), 0)
    return grouped


def _add_namespace_to_grouping(groups: dict, namespace_parts: list, index):
    current = namespace_parts[index]

    if not current in groups:
        groups[current] = {}

    if index == len(namespace_parts) - 1:
        groups[current] = {}
    else:
        _add_namespace_to_grouping(groups[current], namespace_parts, index + 1)


def _get_files_in_namespace(namespace: Namespace):
    for member in namespace.members:
        yield member.file_path


def _get_script_dependencies(project: Project):
    dependencies = {}

    for file_path in project.script_contents.keys():
        dependencies[file_path] = set()

    for member in project.get_members_recursive():
        member_dependencies = set(map(lambda member: member.file_path, member.member_dependencies))
        dependencies[member.file_path] = dependencies[member.file_path].union(member_dependencies).union(member.namespace_dependencies_not_in_members)

    return dependencies