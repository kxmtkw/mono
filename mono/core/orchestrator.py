from mono.agent.agent import Agent
from mono.builder.builder import AgentBuilder

from mono.model.manager import ModelManager

from mono.interface.base import BaseInterface
from mono.interface.terminal import TerminalInterface

from mono.tools.manager import ToolManager
from mono.utils import Logger, MonoError

logger = Logger("orchestrator")


class Orchestrator:

	def __init__(self) -> None:
		logger.info("Hello World!")

		self.interface = TerminalInterface()
		self.interface.start()

		self.model = ModelManager()
		self.tools = ToolManager()

		self.builder = AgentBuilder(self.model, self.tools)
	

	def run(self, filepath: str):

		try:
			agent = self.builder.build(filepath, self.interface)
		except MonoError as e:
			logger.error(f"Failed to run root agent because agent could not be built from {filepath}. {str(e)}")
			self.interface.error(f"{e}")
			return
		
		logger.info(f"Running agent({agent.id}).")

		agent.activate()

		try:
			agent.run()
		except MonoError as e:
			logger.error(f"Root agent({agent.id}) failed. {e}")
			self.interface.error(f"{e}")
			return
		
		agent.deactivate()
		self.interface.end()

		logger.info("Bye World!")
	




	
