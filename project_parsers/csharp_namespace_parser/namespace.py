from project_parsers.csharp_namespace_parser import csharp_parser
from project_parsers.csharp_namespace_parser.member import Member


class Namespace:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.scripts = set()

    def parse_contents(self, contents, file_path):
        self.scripts.add(file_path)
        for data in csharp_parser.get_root_members(contents, file_path):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], data[3], file_path, self))

    def ensure_all_using_statements_accounted_for(self, all_scripts: dict, all_namespaces: list):
        all_namespace_names = [namespace.get_namespace() for namespace in all_namespaces]
        for member in self.members:
            namespaces_used = set(csharp_parser.get_all_namespaces_in_use(all_scripts[member.file_path])).intersection(all_namespace_names)
            member.ensure_depends_on_namespaces(namespaces_used)

    def get_members_recursive(self):
        for member in self.members:
            for member in member.get_members_recursive():
                yield member

    def find_dependencies(self, all_members):
        for member in self.members:
            member.find_dependencies(all_members)

    def get_full_namespace_parts(self):
        if self.name == "none":
            return []
        return self.name.split(".")
        
    def get_full_namespace(self):
        return ".".join(self.get_full_namespace_parts())

    def pretty_print(self, indent=0):
        print("\t" * indent + f"{self.name} (namespace)")
        for member in self.members:
            member.pretty_print(indent + 1)

    def get_namespace(self):
        return self.get_full_namespace()

    def __str__(self):
        return f"Namespace({self.name})"

    def __repr__(self):
        return str(self)