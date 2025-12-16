from dependency_file_merger import update_file
from project_parsers.csharp_namespace_parser.json_writer import get_as_dict
from project_parsers.csharp_namespace_parser.project import Project


class Parser:
    def __init__(self, project_path: str, output_path: str) -> None:
        self.project_path = project_path
        self.output_path = output_path

    def update_dependencies_file(self):
        proj = Project(self.project_path)
        update_file(self.output_path, get_as_dict(proj))