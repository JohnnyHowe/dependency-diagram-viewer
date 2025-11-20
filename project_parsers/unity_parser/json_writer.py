import json
import re
from project import Project
from namespace import Namespace


def write(file_path: str, project: Project):
    with open(file_path, "w") as file:
        d = _get_as_dict(project)
        s = json.dumps(d, indent=4)
        file.write(s)


def _get_as_dict(project: Project) -> dict:

    namespaces_to_contained_files = {}
    for namespace in project.namespaces.values():
        namespaces_to_contained_files[namespace.name] = set(_get_files_in_namespace(namespace))

    script_dependencies = _get_script_dependencies(project)

    data = {
        "path": "",
        "name": "",
        "folders": [],
        "scripts": []
    }

    for namespace in project.namespaces.values():
        scripts = []
        for file_path in namespaces_to_contained_files[namespace.name]:
            name = re.split(r"[\\/]", file_path)[-1]
            scripts.append({
                "path": file_path,
                "name": name,
                "full_name": file_path,
                "dependencies": list(script_dependencies[file_path])
            })

        data["folders"].append({
            "path": namespace.name,
            "name": namespace.name,
            "folders": [],
            "scripts": scripts,
        })
        
    return data


def _get_files_in_namespace(namespace: Namespace):
    for member in namespace.members:
        yield member.file_path


def _get_script_dependencies(project: Project):
    dependencies = {}

    for file_path in project.script_contents.keys():
        dependencies[file_path] = set()

    for member in project.get_members_recursive():
        member_dependencies = set(map(lambda member: member.file_path, member.dependencies))
        dependencies[member.file_path] = dependencies[member.file_path].union(member_dependencies)

    return dependencies