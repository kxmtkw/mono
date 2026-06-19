from enum import Enum
import os
from datetime import datetime
from pathlib import Path

class Level(Enum):
	debug = 0
	info = 1
	warn = 2
	critical = 3
	error = 4


class Logger:

	_enabled = True
	_file = Path("logs") / Path(os.getenv("LOG_FILE") or  "mono.log")

	if not _file.parent.exists(): _file.parent.mkdir()
	if not _file.exists(): _file.touch()

	_level = Level.debug


	def __init__(self, domain: str) -> None:
		self._domain = domain


	def log(self, domain: str, msg: str, level: Level):

		if not self._enabled: return
		if level.value < self._level.value: return
			
		timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
		self.logged = f"[{timestamp}] [{level.name}] ({domain}) {msg}\n"

		with open(self._file, "a") as file:
			file.write(self.logged)


	def debug(self, msg: str):
		self.log(self._domain, msg, Level.debug)


	def info(self, msg: str):
		self.log(self._domain, msg, Level.info)


	def warn(self, msg: str):
		self.log(self._domain, msg, Level.warn)


	def critical(self, msg: str):
		self.log(self._domain, msg, Level.critical)
		
		
	def error(self, msg: str):
		self.log(self._domain, msg, Level.error)









