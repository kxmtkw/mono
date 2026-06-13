from enum import Enum 

class MonoError(Exception):
	
	class ErrorLevel(Enum):
		low = 0
		medium = 1
		high = 2

	def __init__(self, msg: str, level: ErrorLevel = ErrorLevel.medium) -> None:
		super().__init__(f"({level.name.upper()}) {msg}")
		self.msg = msg
		self.level = level