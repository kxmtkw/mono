from mono.model.manager import ModelManager
from mono.agent.context import ContextManager

from mono.interface.base import BaseInterface

from .config import AgentConfig


class Agent:


	def __init__(
		self,
		id: int,
		*,
		config: AgentConfig,
		model_manager: ModelManager,
		interface: BaseInterface,
		) -> None:
		
		self.id: int = id
		self.config: AgentConfig = config
		self.context: ContextManager = ContextManager(self.id, self.config)

		self.model: ModelManager = model_manager
		self.interface: BaseInterface = interface

		self.active: bool = False


	def activate(self):
		self.active = True


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
			response = self.model.ask(self.id, prompt)

			self.context.add_message("user", user_input)

			self.context.add_message("model", response.response)

			self.interface.tell(self.config.name, response.response)





