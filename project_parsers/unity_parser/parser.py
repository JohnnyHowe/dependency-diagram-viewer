import json_parser
from project_parsers.unity_parser.json_writer import get_as_dict
from project_parsers.unity_parser.project import Project


class Parser:
    def __init__(self, project_path: str, output_path: str) -> None:
        self.project_path = project_path
        self.output_path = output_path

    def update_dependencies_file(self):
        proj = Project(self.project_path)
        json_parser.update_file(self.output_path, get_as_dict(proj))