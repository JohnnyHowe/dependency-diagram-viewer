from pathlib import Path
from project_parsers.csharp_namespace_parser import csharp_parser


class Member:
    def __init__(self, name, member_type, contents, definition, file_path, parent):
        self.definition = definition
        self.parent = parent
        self.name = name
        self.member_type = member_type
        self.contents = contents
        self.file_path = file_path
        self.members = []
        self.namespace_dependencies_not_in_members = set()
        self._parse()

    def _parse(self):
        self.file_contents = csharp_parser.load_contents(self.file_path)

        for data in csharp_parser.get_root_members(self.contents, self.file_path):
            assert data[0] != "namespace" "Namespace found but not the root of a file!"
            self.members.append(Member(data[1], data[0], data[2], data[3], self.file_path, self))

    def get_members_recursive(self):
        yield self
        for member in self.members:
            for member in member.get_members_recursive():
                yield member

    def find_dependencies(self, all_members):
        self.member_dependencies = set()

        for member in self.members:
            member.find_dependencies(all_members)

        for member in all_members:
            if member == self:
                continue

            if csharp_parser.depends_on(self.file_contents, self.contents, member.get_full_namespace(), self.get_full_namespace()):
                # TODO filter out items in children but not self
                self.member_dependencies.add(member)

            if csharp_parser.depends_on(self.file_contents, self.definition, member.get_full_namespace(), self.get_full_namespace()):
                self.member_dependencies.add(member)

    def get_full_namespace_parts(self):
        return self.parent.get_full_namespace_parts() + [self.name]

    def get_full_namespace(self):
        return ".".join(self.get_full_namespace_parts())

    def get_namespace(self):
        return self.parent.get_namespace()

    def pretty_print(self, indent=0):
        dependency_names = ", ".join(map(lambda d: d.name, self.member_dependencies))
        print("\t" * indent + f"({self.member_type}) {self.name:<48} depends on {dependency_names}")
        for member in self.members:
            member.pretty_print(indent + 1)
        
    def ensure_depends_on_namespaces(self, namespaces: list[str]):
        for namespace in namespaces:
            self.ensure_depends_on_namespace(namespace)

    def ensure_depends_on_namespace(self, namespace_name: str):
        if namespace_name == "none" or namespace_name == "":
            return

        if self._already_depends_on_namespace_recursive(namespace_name):
            return

        self._add_to_namespace_dependencies(namespace_name)

    def _add_to_namespace_dependencies(self, namespace: str):
        self.namespace_dependencies_not_in_members.add(namespace)
        for member in self.members:
            member._add_to_namespace_dependencies(namespace)

    def _already_depends_on_namespace_recursive(self, namespace: str) -> bool:
        if namespace in self.get_full_namespace():
            return True
        for member in self.get_members_recursive():
            for dependency in member.member_dependencies:
                if dependency.get_namespace() == namespace:
                    return True
        return False

    def __str__(self):
        return f"{self.member_type} {self.name}"

    def __repr__(self):
        return str(self)