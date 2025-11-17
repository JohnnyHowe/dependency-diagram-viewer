from diagram.diagram_item import DiagramItem


class DiagramModule(DiagramItem):
    def __init__(self, path, center_position):
        super().__init__(path, center_position)
        self.folders = []
        self.scripts = []