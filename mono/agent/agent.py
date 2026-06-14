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

			prompt = self.context.make_prompt("user", user_input)
			response = self.model.ask(self.id, request=prompt)

			self.context.add_message("user", user_input)

			while response.mode == "think":
				self.context.add_message("thought", response.thought)
				response =self.modelManager.ask(self.id, request=prompt)

			self.context.add_message("model", response.response)

			self.interface.tell(self.config.name, response.response)





