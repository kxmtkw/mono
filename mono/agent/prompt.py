from mono.agent.config import AgentIdentity

from mono.tools.toolbox import ToolSpace
from mono.utils import Logger

logger = Logger("prompt")

class PromptManager():


	def __init__(self, id: int, system: str,  identity: AgentIdentity) -> None:

		self.agent_id = id
		self.identity: AgentIdentity = identity

		self.base = "\n".join(
			[
				"<system>",
				system,
				"</system>",
				"<identity>",
				f"- Name: {self.identity.name}",
				f"- Id: {self.agent_id}",
				self.identity.intro,
				"<personality>",
				self.identity.personality,
				"</personality>",
				"<behaviour>",
				self.identity.behavior,
				"</behavior>",
				"<constraints>",
				self.identity.constraints,
				"</constraints>",
				"</identity>"
			]
		)
		logger.debug("Assembled base prompt")

		self.chat: list[str] = []
		self.toolspaces: list[ToolSpace] = []
		self.toolspaces_str: str = ""


	def update(
		self, 
		*, 
		chat: list[str] | None = None,
		toolspaces: list[ToolSpace] | None = None
		):
		
		if chat: 
			self.chat = chat
			logger.debug(f"Updated chat for agent({self.agent_id})")
		if toolspaces: 
			self.toolspaces = toolspaces
			self.toolspaces_str = self._format_tools(toolspaces)
			logger.debug(f"Updated tools section for agent({self.agent_id})")


	def make_prompt(self, role: str, mesg: str) -> str:
		
		prompt = "\n".join(
			[
				self.base,
				"<tools>",
				self.toolspaces_str,
				"</tools>",
				"<session>",
				"<chat>",
				*self.chat,
				"</chat>",
				f"<prompt source={role}>",
				mesg,
				"</prompt>",
				"</session>",
			]
		)

		with open("logs/prompt.txt", "w") as file:
			file.write(prompt + "\n"*10)

		logger.debug(f"Made prompt for agent({self.agent_id})")
		return prompt



	def _format_tools(self, tool_spaces: list[ToolSpace]) -> str:

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
