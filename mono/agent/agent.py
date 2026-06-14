from mono.model.manager import ModelManager
from mono.agent.context import ContextManager

from mono.interface.base import BaseInterface

class Agent:

	def __init__(
		self,
		id: int,
		modelManager: ModelManager,
		context: ContextManager,
		interface: BaseInterface,
		*,
		name: str,
		identity: str,
		model: str
		) -> None:
		
		self.modelManager: ModelManager = modelManager
		self.context: ContextManager = context
		self.interface: BaseInterface = interface

		self.id: int = id
		self.name: str = name
		self.identity: str = identity
		self.model: str = model
		
		self.active: bool = False


	def activate(self):
		self.active = True


	def deactivate(self):
		self.active = False


	def run(self):

		while self.active:

			user_input = self.interface.listen()

			prompt = self.context.make_prompt("user", user_input)
			response = self.modelManager.ask(self.id, request=prompt)

			self.context.add_message("user", user_input)

			while response.mode == "think":
				self.context.add_message("thought", response.thought)
				response =self.modelManager.ask(self.id, request=prompt)

			self.context.add_message("model", response.response)

			self.interface.tell(self.name, response.response)





