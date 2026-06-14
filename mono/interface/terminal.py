from mono.interface.base import BaseInterface


class Color:

	reset = "\033[0m"

	black   = "\033[30m"
	red     = "\033[31m"
	green   = "\033[32m"
	yellow  = "\033[33m"
	blue    = "\033[34m"
	magenta = "\033[35m"
	cyan    = "\033[36m"
	white   = "\033[37m"

	bright_black   = "\033[90m"
	bright_red     = "\033[91m"
	bright_green   = "\033[92m"
	bright_yellow  = "\033[93m"
	bright_blue    = "\033[94m"
	bright_magenta = "\033[95m"
	bright_cyan    = "\033[96m"
	bright_white   = "\033[97m"

	@classmethod
	def print(cls, msg: str, color: str, *, end="\n"):
		print(f"{color}{msg}{Color.reset}", end=end)

	@staticmethod
	def colorify(text:str, color: str):
		return f"{color}{text}{Color.reset}"


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