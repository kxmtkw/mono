from typing import Literal
from mono.agent.config import AgentConfig
from mono.tools.toolbox import ToolSpace
from mono.utils import logger

class ContextManager():


	def __init__(self, id: int, system: str, config: AgentConfig) -> None:
		
		self.system = system

		self.agent = id
		self.config: AgentConfig = config
		self.context: list[str] = []

		self.history: list[str] = []
		self.chat: list[str] = []


	def initialize(self, toolbox: list[ToolSpace]):

		self.base = "\n".join(
			[
				"<system>",
				self.system,
				"# Identity",
				f"- Name: {self.config.name}",
				f"- Id: {id}",
				f"- Model: {self.config.model}",
				self.config.identity,
				f"## Personality",
				self.config.personality,
				f"## Behaviour",
				self.config.behaviour,
				"# Tools",
				self.format_tools(toolbox),
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
	

	def format_tools(self, tool_spaces: list[ToolSpace]) -> str:

		output = []
		
		for space in tool_spaces:
			output.append(f"## {space.namespace}")
			
			for name, spec in space.tools.items():
				output.append(f"#### {name}")
				output.append(f"{spec.info}")
				
				for arg_name, (arg_type, arg_info) in spec.arguments.items():
					# Get the type name from the type object
					type_name = arg_type.__name__ if hasattr(arg_type, '__name__') else str(arg_type)
					output.append(f"- {arg_name} ({type_name}): {arg_info}")
				
				output.append("")
				
		return "\n".join(output).strip()
