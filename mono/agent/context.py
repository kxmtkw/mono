from typing import Literal
from mono.agent.config import AgentConfig
from mono.utils import logger

class ContextManager():


	def __init__(self, id: int, system: str, config: AgentConfig) -> None:
		self.system = system

		self.agent = id
		self.config: AgentConfig = config
		self.context: list[str] = []
		self.history: list[str] = []
		self.chat: list[str] = []

		self.base = "\n".join(
			[
				"<system>",
				system,
				"# Identity",
				f"- Name: {self.config.name}",
				f"- Id: {id}",
				f"- Model: {self.config.model}",
				self.config.identity,
				f"## Personality",
				self.config.personality,
				f"## Behaviour",
				self.config.behaviour,
				"</system>"
			]
		)


	def add_message(self, role: str, mesg: str):
		"Add a message to the agent's chat. Ignores if agent is not registered."

		self.chat.append(f"{role.upper()}: {mesg}")

		logger.debug("context", f"Updated chat of agent({self.agent}) with role '{role}'.")


	def make_prompt(self, role: str, msg: str) -> str:
		"Assemble a prompt. Raises ContextError if agent not registered."

		prompt = "\n".join(
			[
				self.base,
				"<user>",
				"# Chat",
				*self.chat,
				"# Prompt",
				f"{role.upper()}: {msg}",
				"</user>"
			]
		)

		logger.info("context", f"Assembling prompt for agent({self.agent}).")

		return prompt
