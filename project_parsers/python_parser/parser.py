from .folder import Folder
import json_parser


class Parser:
    def __init__(self, project_path: str, output_path: str) -> None:
        self.project_path = project_path
        self.output_path = output_path

    def update_dependencies_file(self):
        root = Folder(self.project_path)
        d = root.as_dict()
        json_parser.update_file(self.output_path, d)