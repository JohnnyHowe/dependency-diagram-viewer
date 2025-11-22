class ProjectScript:
    def __init__(self, path):
        self.path = path
        self.full_name = None
        self.name = None 
        self.dependencies = []

    def get_all_dependency_pairs(self):
        for dependency in self.dependencies:
            yield (self, dependency)

    def get_as_dict(self) -> dict:
        d = { "path": self.path, "full_name": self.full_name, "name": self.name, "dependencies": [] }
        for dependency in self.dependencies:
            d["dependencies"].append(dependency.full_name)
        return d

    def __str__(self):
        return f"ProjectScript at {self.path}"

    def __repr__(self):
        return str(self)