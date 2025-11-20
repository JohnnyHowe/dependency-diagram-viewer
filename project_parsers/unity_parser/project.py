import os
import csharp_parser
from namespace import Namespace
from member import Member


class Project:
    def __init__(self, path):
        self.path = path
        self.namespaces = {"none": Namespace("none")}
        self._parse()
        self.pretty_print()

    def _parse(self):
        for root, dir_names, file_names in os.walk(self.path):
            for file_name in file_names:
                if csharp_parser.is_script(file_name):
                    self._parse_file(os.path.join(root, file_name))
                
    def _parse_file(self, file_path):
        contents = csharp_parser.load_contents(file_path)
        root_members = csharp_parser.get_root_members(contents)

        for data in root_members:
            self._add_script_root_member(*data, file_path)

    def _add_script_root_member(self, member_type, name, contents, file_path):
        if member_type != "namespace":
            self.namespaces["none"].members.append(Member(name, member_type, contents, file_path))
            pass
        elif name not in self.namespaces:
            namespace = Namespace(name)
            namespace.parse_contents(contents, file_path)
            self.namespaces[name] = namespace

    def pretty_print(self):
        print(f"Project at {self.path}")
        for namespace in self.namespaces.values():
            namespace.pretty_print(1)