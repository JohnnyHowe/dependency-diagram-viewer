import csharp_parser


class Member:
    def __init__(self, name, member_type, contents, file_path):
        self.name = name
        self.member_type = member_type
        self.contents = contents
        self.file_path = file_path

        self.members = []

        self._parse()

    def _parse(self):
        for data in csharp_parser.get_root_members(self.contents):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], self.file_path))

    def pretty_print(self, indent=0):
        print("\t" * indent + f"{self.name} ({self.member_type})")
        for member in self.members:
            member.pretty_print(indent + 1)

    def __str__(self):
        return f"{self.member_type} {self.name}"

    def __repr__(self):
        return str(self)