from abc import abstractmethod, ABC

class BaseInterface(ABC):

	def __init__(self) -> None:
		super().__init__()


	@abstractmethod
	def start(self):
		"Start the interface."
		pass


	@abstractmethod
	def end(self):
		"End the interface."
		pass


	@abstractmethod
	def listen(self) -> str | None:
		"Get user input. Called by the agent."
		pass


	@abstractmethod
	def tell(self, source: str, msg: str):
		"Called when something is to be reported to the user."
		pass


	@abstractmethod
	def ask(self, source: str, msg: str, options: tuple[str]) -> str:
		"Called when something is to asked from the user."
		pass


	@abstractmethod
	def error(self, msg: str):
		"Called when something is goes wrong"
		pass


	@abstractmethod
	def state(self, msg: str):
		"Called when state updates."
		pass

