from mono.agent.agent import Agent

from mono.modules.context import ContextModule
from mono.modules.model import ModelModule

from mono.agent.builder import AgentBuilder

from mono.utils import logger, MonoError

from mono.core.interface import BaseInterface


class Orchestrator:

	def __init__(self, interface: BaseInterface) -> None:
		self.builder = AgentBuilder()
		self.interface = interface
		logger.setup()

	
	def run(self, filepath: str):

		try:
			agent = self.builder.build(filepath)
		except MonoError as e:
			logger.error("orchestrator", f"Failed to run agent because agent could not be built from {filepath}. {str(e)}")
			return
		
		self.interface.start()

		logger.info("orchestrator", f"Running agent({agent.id}).")

		agent.activate()
		self.loop(agent)


	def loop(self, agent: Agent):

		context = ContextModule()
		model = ModelModule()

		while agent.active:

			user_input = self.interface.listen()

			prompt = context.make_prompt(agent, role="user", msg=user_input)
			response = model.ask(agent, request=prompt)

			context.add_message(agent, role="user", mesg=user_input)

			while response.mode == "think":
				context.add_message(agent, role="thought", mesg=response.thought)
				response = model.ask(agent, request=prompt)

			context.add_message(agent, role="model", mesg=response.response)

			self.interface.tell(agent.name, response.response)


	
