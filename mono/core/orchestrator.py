from mono.agent.agent import Agent

from mono.model.manager import ModelManager

from mono.agent.builder import AgentBuilder

from mono.utils import logger, MonoError

from mono.interface.base import BaseInterface


class Orchestrator:

	def __init__(self, interface: BaseInterface) -> None:
		self.model = ModelManager()
		self.builder = AgentBuilder(self.model)
		self.interface = interface
		logger.setup()

	
	def run(self, filepath: str):

		try:
			agent = self.builder.build(filepath, self.interface)
		except MonoError as e:
			logger.error("orchestrator", f"Failed to run agent because agent could not be built from {filepath}. {str(e)}")
			return
		
		self.interface.start()

		logger.info("orchestrator", f"Running agent({agent.id}).")

		agent.activate()
		agent.run()





	
