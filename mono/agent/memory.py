
from mono.utils import Logger

logger = Logger("memory")


class MemoryManager():

	def __init__(self, id: int) -> None:
		self.agent_id = id
		self.chat: list[str] = []

	def add_message(self, role: str, msg: str):
		logger.debug(f"Updated chat by role '{role}'")
		self.chat.append(f"<{role.upper()}> {msg}")

	def get_chat(self) -> list[str]:
		return self.chat
	
	
