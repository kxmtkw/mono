from enum import Enum

class Level(Enum):
	debug = 0
	info = 1
	warn = 2
	critical = 3
	error = 4


_enabled = True
_file = "mono.log"
_level = Level.debug


def setup(enabled: bool = _enabled, filepath: str = _file, level = _level):

	global _enabled, _file, _level

	_enabled = enabled
	_file = filepath
	_level = level

	with open(_file, "w") as file:
		pass


def log(domain: str, msg: str, level: Level):

	if not _enabled: return
	if level.value < _level.value: return
		
	logged = f"[{level.name}] ({domain}) {msg}\n"

	with open(_file, "a") as file:
		file.write(logged)


def debug(domain: str, msg: str):
	log(domain, msg, Level.debug)


def info(domain: str, msg: str):
	log(domain, msg, Level.info)


def warn(domain: str, msg: str):
	log(domain, msg, Level.warn)


def critical(domain: str, msg: str):
	log(domain, msg, Level.critical)
	
	
def error(domain: str, msg: str):
	log(domain, msg, Level.error)