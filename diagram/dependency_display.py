from diagram.diagram_item import DiagramItem


class DependencyDisplay:
    source: DiagramItem
    target: DiagramItem

    pair: tuple[DiagramItem]
    inverse_pair: tuple[DiagramItem]

    # none (normal), "transitive", "mutual"
    dependecy_type: str = None

    def __init__(self, source: DiagramItem, target: DiagramItem, depedency_type: str = None) -> None:
        self.source = source
        self.target = target
        self.dependecy_type = depedency_type

        self.pair = (source, target)
        self.inverse_pair = (target, source)