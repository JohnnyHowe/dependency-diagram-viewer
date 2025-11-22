import os

from project_parsers.unity_parser.member import Member
from project_parsers.unity_parser.namespace import Namespace
from project_parsers.unity_parser import csharp_parser


class Project:
    def __init__(self, path):
        self.path = path
        self.namespaces = {"none": Namespace("none")}
        self._parse()

    def _parse(self):
        self.script_contents = {}
        for root, dir_names, file_names in os.walk(self.path):
            for file_name in file_names:
                if csharp_parser.is_script(file_name):
                    self._parse_file(os.path.join(root, file_name))
        self.cull_empty_namespaces()
        self._find_dependencies()
        self.ensure_all_namespaces_accounted_for()

    def cull_empty_namespaces(self):
        to_cull = []
        for key, value in self.namespaces.items():
            if len(value.members) == 0:
                to_cull.append(key)
        for key in to_cull:
            del self.namespaces[key]
                
    def _parse_file(self, file_path):
        contents = csharp_parser.load_contents(file_path)
        self.script_contents[file_path] = contents
        root_members = csharp_parser.get_root_members(contents, file_path)

        for data in root_members:
            self._add_script_root_member(*data, file_path)

    def _add_script_root_member(self, member_type, name, contents, definition, file_path):
        # member isn't in a namespace :/
        if member_type != "namespace": 
            namespace = self.namespaces["none"]
            namespace.scripts.add(file_path)
            namespace.members.append(Member(name, member_type, contents, definition, file_path, namespace))
            return

        if name not in self.namespaces:
            self.namespaces[name] = Namespace(name)
        self.namespaces[name].parse_contents(contents, file_path)

    def _find_dependencies(self):
        all_members = list(self.get_members_recursive())
        for namespace in self.namespaces.values():
            namespace.find_dependencies(all_members)

    def get_members_recursive(self):
        for namespace in self.namespaces.values():
            for member in namespace.get_members_recursive():
                yield member

    def ensure_all_namespaces_accounted_for(self):
        for namespace in self.namespaces.values():
            namespace.ensure_all_using_statements_accounted_for(self.script_contents, self.namespaces.values())

    def pretty_print(self):
        print(f"Project at {self.path}")
        for namespace in self.namespaces.values():
            namespace.pretty_print(1)