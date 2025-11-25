from pygame import Vector2
from diagram.diagram_item import DiagramItem


class DependencyDisplay:
	source: DiagramItem
	target: DiagramItem

	pair: tuple[DiagramItem]
	inverse_pair: tuple[DiagramItem]

	# none (any), "direct (script to script)", "transitive", "mutual"
	dependency_type: str = None

	def __init__(self, source: DiagramItem, target: DiagramItem, dependency_type: str = None) -> None:
		self.source = source
		self.target = target
		self.dependency_type = dependency_type

		self.pair = (source, target)
		self.inverse_pair = (target, source)

	def get_start_position(self) -> Vector2:
		if self.dependency_type != "mutual":
			return self.source.rect.midtop

		left = self.source if self.source.rect.center[0] < self.target.rect.center[0] else self.target
		return left.rect.midright

	def get_end_position(self) -> Vector2:
		if self.dependency_type != "mutual":
			return self.target.rect.midbottom

		left = self.source if self.source.rect.center[0] < self.target.rect.center[0] else self.target
		right = self.source if left == self.target else self.target
		return right.rect.midleft