from mono.model.manager import ModelManager
from mono.agent.context import ContextManager

from mono.interface.base import BaseInterface
from mono.tools.manager import ToolManager

from .config import AgentConfig

from mono.utils import MonoError


class Agent:


	def __init__(
		self,
		id: int,
		*,
		config: AgentConfig,
		system_prompt: str,
		model_manager: ModelManager,
		tool_manager: ToolManager,
		interface: BaseInterface,
		) -> None:
		
		self.id: int = id
		self.config: AgentConfig = config
		self.context: ContextManager = ContextManager(self.id, system_prompt, self.config)

		self.model: ModelManager = model_manager
		self.tools: ToolManager = tool_manager

		self.interface: BaseInterface = interface

		self.active: bool = False


	def activate(self):
		self.active = True
		self.context.initialize(self.tools.get_agent_toolbox(self.id))


	def deactivate(self):
		self.active = False


	def run(self):

		while self.active:

			user_input = self.interface.listen()

			if user_input is None:
				self.deactivate()
				return

			self.interface.state(f"Responding")

			prompt = self.context.make_prompt("user", user_input)
			
			try:
				response = self.model.ask(self.id, prompt)
			except MonoError as e:
				self.interface.error(str(e))
				continue

			self.context.add_message("user", user_input)

			
			with open("mono.prompt", "a") as file:
				file.write(prompt)
				file.write("\n"*10)
			

			while response.tool_called:
				
				self.interface.state("Executing")

				result = self.tools.execute(
					self.id,
					response.tool_namespace,
					response.tool_func_name,
					response.convert_to_dict(response.tool_args)
				)

				prompt = self.context.make_prompt("tools", f"Success: {result.success}\n{result.output}")

				with open("mono.prompt", "a") as file:
					file.write(prompt)
					file.write("\n"*10)

				response.tool_called = False

				try:
					response = self.model.ask(self.id, prompt)
				except MonoError as e:
					self.interface.error(str(e))
					continue

				self.context.make_prompt("tools", f"Success: {result.success}\n{result.output}")


			self.context.add_message("model", response.response)

			self.interface.tell(self.config.name, response.response)





