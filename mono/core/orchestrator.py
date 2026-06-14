from mono.agent.agent import Agent
from mono.agent.builder import AgentBuilder

from mono.model.manager import ModelManager

from mono.interface.base import BaseInterface
from mono.interface.terminal import TerminalInterface

from mono.utils import logger, MonoError



class Orchestrator:

	def __init__(self) -> None:
		self.model = ModelManager()
		self.builder = AgentBuilder(self.model)
		self.interface = TerminalInterface()
		logger.setup()

	
	def run(self, filepath: str):

		try:
			agent = self.builder.build(filepath, self.interface)
		except MonoError as e:
			logger.error("orchestrator", f"Failed to run root agent because agent could not be built from {filepath}. {str(e)}")
			self.error(e)
			return
		
		self.interface.start()

		logger.info("orchestrator", f"Running agent({agent.id}).")

		agent.activate()

		try:
			agent.run()
		except MonoError as e:
			logger.error("orchestrator", f"Root agent({agent.id}) failed. {str(e)}")
			self.error(e)
			return
		
		self.interface.end()


	def error(self, err: MonoError):
		print(f"[Error] ({err.level.name}) {err.msg}")
	




	
