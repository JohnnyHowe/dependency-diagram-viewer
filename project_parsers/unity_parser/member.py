import csharp_parser


class Member:
    def __init__(self, name, member_type, contents, definition, file_path, parent):
        self.definition = definition
        self.parent = parent
        self.name = name
        self.member_type = member_type
        self.contents = contents
        self.file_path = file_path

        self.members = []

        self._parse()

    def _parse(self):
        self.file_contents = csharp_parser.load_contents(self.file_path)

        for data in csharp_parser.get_root_members(self.contents):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], data[3], self.file_path, self))

    def get_members_recursive(self):
        yield self
        for member in self.members:
            for member in member.get_members_recursive():
                yield member

    def find_dependencies(self, all_members):
        self.dependencies = set()

        for member in self.members:
            member.find_dependencies(all_members)

        for member in all_members:
            if member == self:
                continue

            if csharp_parser.depends_on(self.file_contents, self.contents, member.get_full_namespace(), self.get_full_namespace()):
                # TODO filter out items in children but not self
                self.dependencies.add(member)

            if csharp_parser.depends_on(self.file_contents, self.definition, member.get_full_namespace(), self.get_full_namespace()):
                self.dependencies.add(member)

    def get_full_namespace(self):
        return self.parent.get_full_namespace() + "." + self.name

    def pretty_print(self, indent=0):
        print("\t" * indent + f"({self.member_type}) {self.name:<48} depends on {", ".join(map(lambda d: d.name, self.dependencies))}")
        for member in self.members:
            member.pretty_print(indent + 1)

    def __str__(self):
        return f"{self.member_type} {self.name}"

    def __repr__(self):
        return str(self)