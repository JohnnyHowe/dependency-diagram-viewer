from diagram.diagram_item import DiagramItem


class DiagramScript(DiagramItem):
    def __init__(self, full_name, name, path, center_position):
        super().__init__(path, center_position)
        self.dependencies = []
        self.full_name = full_name
        self.name = name