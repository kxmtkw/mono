
class Agent:

	def __init__(
		self,
		id: int,
		*,
		name: str,
		identity: str
		) -> None:
		
		self.id: int = id
		self.name = name
		self.identity = identity
		
		self.active: bool = False

	def activate(self):
		self.active = True



