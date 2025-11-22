
from dependency_file_merger import update_file
from project_parsers.godot.gd_module import GdModule


class GodotParser:
    def __init__(self, project_path: str, output_path: str) -> None:
        self.project_path = project_path
        self.output_path = output_path

    def update_dependencies_file(self):
        root = GdModule(self.project_path)
        root.update_internal_dependencies()
        update_file(self.output_path, root.get_as_dict())