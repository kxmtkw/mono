from abc import ABC, abstractmethod
from .response import ModelResponse

class BaseModelProvider:

	def __init__(self) -> None:
		pass

	@classmethod
	@abstractmethod
	def name(cls) -> str:
		pass

	@abstractmethod
	def ask(self, msg: str) -> ModelResponse:
		pass
