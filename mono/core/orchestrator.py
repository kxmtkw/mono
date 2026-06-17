from mono.agent.agent import Agent
from mono.builder.builder import AgentBuilder

from mono.model.manager import ModelManager

from mono.interface.base import BaseInterface
from mono.interface.terminal import TerminalInterface

from mono.tools.manager import ToolManager
from mono.utils import logger, MonoError



class Orchestrator:

	def __init__(self) -> None:
		logger.setup()

		self.interface = TerminalInterface()
		self.interface.start()

		self.model = ModelManager()
		self.tools = ToolManager()

		self.builder = AgentBuilder(self.model, self.tools)
	

	def run(self, filepath: str):

		try:
			agent = self.builder.build(filepath, self.interface)
		except MonoError as e:
			logger.error("orchestrator", f"Failed to run root agent because agent could not be built from {filepath}. {str(e)}")
			self.interface.error(f"{e}")
			return
		
		logger.info("orchestrator", f"Running agent({agent.id}).")

		agent.activate()

		try:
			agent.run()
		except MonoError as e:
			logger.error("orchestrator", f"Root agent({agent.id}) failed. {e}")
			self.interface.error(f"{e}")
			return
		
		agent.deactivate()
		self.interface.end()
	




	
