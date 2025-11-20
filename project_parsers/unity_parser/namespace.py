import csharp_parser
from member import Member


class Namespace:
    def __init__(self, name):
        self.name = name
        self.members = []

    def parse_contents(self, contents, file_path):
        for data in csharp_parser.get_root_members(contents):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], file_path))

    def pretty_print(self, indent=0):
        print("\t" * indent + f"{self.name} (namespace)")
        for member in self.members:
            member.pretty_print(indent + 1)

    def __str__(self):
        return f"Namespace({self.name})"

    def __repr__(self):
        return str(self)