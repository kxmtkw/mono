from abc import abstractmethod, ABC

class BaseInterface(ABC):

	def __init__(self) -> None:
		super().__init__()


	@abstractmethod
	def start(self):
		pass


	@abstractmethod
	def end(self):
		pass


	@abstractmethod
	def listen(self) -> str | None:
		pass


	@abstractmethod
	def tell(self, source: str, msg: str):
		pass


	@abstractmethod
	def ask(self, source: str, msg: str, options: tuple[str]) -> str:
		pass

