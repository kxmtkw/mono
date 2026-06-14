from abc import ABC, abstractmethod
from .response import ModelResponse

class BaseModelProvider:

	def __init__(self) -> None:
		pass

	@abstractmethod
	def name(self) -> str:
		pass

	@abstractmethod
	def start(self):
		pass

	@abstractmethod
	def end(self):
		pass

	@abstractmethod
	def ask(self, msg: str) -> ModelResponse:
		pass
