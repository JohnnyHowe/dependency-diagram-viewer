import csharp_parser
from member import Member


class Namespace:
    def __init__(self, name):
        self.name = name
        self.members = []

    def parse_contents(self, contents, file_path):
        for data in csharp_parser.get_root_members(contents):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], data[3], file_path, self))

    def get_members_recursive(self):
        for member in self.members:
            for member in member.get_members_recursive():
                yield member

    def find_dependencies(self, all_members):
        for member in self.members:
            member.find_dependencies(all_members)
        
    def get_full_namespace(self):
        return self.name

    def pretty_print(self, indent=0):
        print("\t" * indent + f"{self.name} (namespace)")
        for member in self.members:
            member.pretty_print(indent + 1)

    def __str__(self):
        return f"Namespace({self.name})"

    def __repr__(self):
        return str(self)