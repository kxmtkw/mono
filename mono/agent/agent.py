from typing import Any

from mono.agent.memory import MemoryManager
from mono.agent.prompt import PromptManager

from mono.model.manager import ModelManager

from mono.interface.base import BaseInterface
from mono.model.response import ModelResponse, ToolCall
from mono.tools.manager import ToolManager

from .config import AgentConfig

from mono.utils import MonoError


class Agent:


	def __init__(
		self,
		*,
		id: int,
		system: str,
		config: AgentConfig,
		modelmanager: ModelManager,
		toolmanager: ToolManager,
		interface: BaseInterface,
		) -> None:
		
		
		self.id: int = id
		self.config: AgentConfig = config

		self.model: ModelManager = modelmanager
		self.tools: ToolManager = toolmanager
		self.interface: BaseInterface = interface

		self.prompt = PromptManager(self.id, system, self.config.identity)
		self.memory = MemoryManager(self.id)

		self.active: bool = False
		
		self.model.register(self.id, self.config.model.name)
		self.tools.register(self.id, self.config.capabilities.allowed_tools)

		self.variables: dict[str, Any] = {} # temporary


	def activate(self):
		self.active = True 
		self.prompt.update(
			chat=self.memory.get_chat(),
			toolspaces=self.tools.get_agent_toolbox(self.id)
		)
		self.current_stage = self.wait_for_input


	def deactivate(self):
		self.active = False


	def run(self):

		while self.active:
			with open("mono.prompt", "a") as file:
				file.write(" " if not self.variables.get("prompt", None) else self.variables["prompt"])
				file.write(" "*20)

			self.current_stage = self.current_stage()

			
	def wait_for_input(self):
		user_input = self.interface.listen()

		if user_input is None:
			self.deactivate()
			return self.wait_for_input
		

		self.prompt.update(chat=self.memory.get_chat())
		self.memory.add_message("user", user_input)

		self.variables["prompt"] = self.prompt.make_prompt("user", user_input)
		return self.ask_model
	


	def ask_model(self):

		self.interface.state(f"responding")
		
		try:
			self.variables["model_response"] = self.model.ask(self.id, self.variables["prompt"] )
		except MonoError as e:
			self.interface.error(str(e))
			return self.wait_for_input


		return self.parse_response


	def parse_response(self):

		self.interface.state(f"parsing")

		response: ModelResponse = self.variables["model_response"]

		if response.toolcalled:
			return self.execute_tool
		
		self.memory.add_message("model", response.response)

		self.interface.tell(self.config.identity.name, response.response)
		
		return self.wait_for_input
	

	def execute_tool(self):
		
		response: ModelResponse = self.variables["model_response"]

		if not response.toolcall: return self.wait_for_input

		if isinstance(response.toolcall, ToolCall):
			response.toolcall = [response.toolcall]

		msg = ""

		for tool in response.toolcall:

			result = self.tools.execute(
				self.id,
				tool.namespace,
				tool.toolname,
				ModelResponse.convert_to_dict(tool.args),
			)
			self.interface.tell("tools", f"Executed: {tool.namespace}::{tool.toolname}")
			msg += f"Tool {tool.namespace}::{tool.toolname} executed. Successful = {result.success}.\n<output>\n{result.output}\n</output>"

		self.prompt.update(chat=self.memory.get_chat())

		self.variables["prompt"] = self.prompt.make_prompt("tools", msg)

		self.memory.add_message("tools", msg)

		return self.ask_model

			



