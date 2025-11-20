import json
from project import Project


def write(file_path: str, project: Project):
    with open(file_path, "w") as file:
        d = _get_as_dict(project)
        s = json.dumps(d, indent=4)
        file.write(s)


def _get_as_dict(project: Project) -> dict:
    return {}