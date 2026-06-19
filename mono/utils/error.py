from enum import Enum
from typing import Optional

class MonoError(Exception):
	
	class ErrorLevel(Enum):
		low = 0
		medium = 1
		high = 2

	def __init__(self, msg: str, level: ErrorLevel = ErrorLevel.low, cause: Optional['MonoError'] = None) -> None:
		super().__init__(f"({level.name.upper()}) {msg}")
		self.msg = msg
		self.level = level
		self.cause = cause

	def __str__(self) -> str:
		return f"({self.level.name.upper()}) {self.msg}"

	def chain(self, depth=0) -> str:
		res = self.__str__()
		if self.cause:
			res += "\n" + "  "*depth + "-> " + self.cause.chain(depth+1)
		return res