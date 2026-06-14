from mono.interface.base import BaseInterface
from mono.utils import Color


class TerminalInterface(BaseInterface):


	def __init__(self) -> None:
		super().__init__()


	def start(self):
		Color.print("[ Mono ] > Running terminal interface.", Color.magenta)
	

	def end(self):
		Color.print("[ Mono ] > Ending interface.", Color.magenta)


	def listen(self) -> str | None:
		try:
			return input(">> ").strip()
		except KeyboardInterrupt:
			print()
			return None


	def tell(self, source: str, msg: str) -> None:
		Color.print(f"[{source}]: {msg}", Color.blue)


	def ask(self, source: str, msg: str, options: tuple[str, ...]) -> str:
		full_prompt = f"[{source}]: {msg} ({'/'.join(options)})"
		Color.print(full_prompt, Color.yellow)

		while True:
			choice = input(">> ").strip()
			if choice in options:
				return choice
			Color.print(f"Invalid choice. Please choose from: {', '.join(options)}", Color.red)