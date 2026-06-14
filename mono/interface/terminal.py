import sys 

from mono.interface.base import BaseInterface
from mono.utils import Color



class TerminalInterface(BaseInterface):


	def __init__(self) -> None:
		super().__init__()
		self.displaying_state = False


	def start(self):
		Color.print("[ Mono ] > Running terminal interface.", Color.magenta)
	

	def end(self):
		self.clear_state()
		Color.print("[ Mono ] > Ending interface.", Color.magenta)


	def listen(self) -> str | None:
		self.clear_state()

		try:
			return input(">> ").strip()
		except KeyboardInterrupt:
			print()
			return None


	def tell(self, source: str, msg: str) -> None:
		self.clear_state()
		Color.print(f"[{source}]: {msg}", Color.blue)


	def ask(self, source: str, msg: str, options: tuple[str, ...]) -> str:

		self.clear_state()

		full_prompt = f"[{source}]: {msg} ({'/'.join(options)})"
		Color.print(full_prompt, Color.yellow)

		while True:
			choice = input(">> ").strip()
			if choice in options:
				return choice
			Color.print(f"Invalid choice. Please choose from: {', '.join(options)}", Color.red)

		
	def error(self, msg: str):
		self.clear_state()

		Color.print(f"[Error] {msg}", Color.red)


	def state(self, msg: str):
		self.clear_state()

		Color.print(f"{msg}...", Color.cyan, end="")
		sys.stdout.flush()
		self.displaying_state = True


	def clear_state(self):
		if self.displaying_state:
			sys.stdout.write("\r\033[K")
			sys.stdout.flush()