from typing import Any

from mono.agent.memory import MemoryManager
from mono.agent.prompt import PromptManager

from mono.model.manager import ModelManager

from mono.interface.base import BaseInterface
from mono.model.response import ModelResponse, ToolCall
from mono.tools.manager import ToolManager

from .config import AgentConfig

from mono.utils import MonoError


class LoopState:
	
	def __init__(self) -> None:
		self.user_input: str
		self.prompt: str
		self.model_response: ModelResponse
		self.tool_calls: list[ToolCall]


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

		self.loopstate = LoopState()



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
			print(f"exe: {self.current_stage.__name__}")
			self.current_stage = self.current_stage()

			
	def wait_for_input(self):
		
		user_input = self.interface.listen()

		if user_input is None:
			self.deactivate()
			return self.wait_for_input
		
		self.loopstate.user_input = user_input

		self.prompt.update(chat=self.memory.get_chat())
		self.loopstate.prompt = self.prompt.make_prompt("user", user_input)

		self.memory.add_message("user", user_input)
		return self.ask_model
	

	def ask_model(self):

		self.interface.state(f"responding")
		
		try:
			model_res = self.model.ask(self.id, self.loopstate.prompt)
		except MonoError as e:
			self.interface.error(str(e))
			return self.wait_for_input

		self.loopstate.model_response = model_res

		return self.parse_response


	def parse_response(self):

		self.interface.state(f"parsing")

		response: ModelResponse = self.loopstate.model_response

		if len(response.toolcall) != 0:
			self.loopstate.tool_calls = response.toolcall
			return self.execute_tool
		
		self.memory.add_message("model", response.response)

		self.interface.tell(self.config.identity.name, response.response)
		
		return self.wait_for_input
	

	def execute_tool(self):
		
		toolcalls = self.loopstate.tool_calls

		msg = ""

		for tool in toolcalls:
			
			args_as_dict = ModelResponse.convert_to_dict(tool.args)
			result = self.tools.execute(
				self.id,
				tool.namespace,
				tool.toolname,
				args_as_dict,
			)
			self.interface.tell("tools", f"Executed: {tool.namespace}::{tool.toolname}")
			msg += f"Tool {tool.namespace}::{tool.toolname} with args {args_as_dict} executed. Successful = {result.success}.\n<output>\n{result.output}\n</output>\n"

		self.prompt.update(chat=self.memory.get_chat())
		self.loopstate.prompt = self.prompt.make_prompt("tools", msg)
		self.memory.add_message("tools", msg)


		return self.ask_model

			



