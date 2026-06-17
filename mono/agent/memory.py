
from mono.utils import logger

class MemoryManager():

	def __init__(self, id: int) -> None:
		self.agent_id = id
		self.chat: list[str] = []

	def add_message(self, role: str, msg: str):
		self.chat.append(f"{role.upper()}: {msg}")

	def get_chat(self) -> list[str]:
		return self.chat
	
	
