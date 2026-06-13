
class Agent:

	def __init__(
		self,
		id: int,
		name: str = "Unknown"
		) -> None:
		
		self.id: int = id
		self.name = name
		self.active: bool = True
