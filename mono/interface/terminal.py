from .base import BaseInterface


class TerminalInterface(BaseInterface):


	def __init__(self) -> None:
		super().__init__()


	def start(self):
		print("[ Mono ] > Running terminal interface.")
	

	def listen(self) -> str:
		return input("> ").strip()


	def tell(self, source: str, msg: str) -> None:
		print(f"[{source}]: {msg}")


	def ask(self, source: str, msg: str, options: tuple[str, ...]) -> str:
		full_prompt = f"[{source}]: {msg} ({'/'.join(options)}): "
		while True:
			choice = input(full_prompt).strip()
			if choice in options:
				return choice
			print(f"Invalid choice. Please choose from: {', '.join(options)}")