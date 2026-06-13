from .agent import Agent
import json

from mono.modules.context import ContextModule
from mono.modules.model import ModelModule

from mono.utils import logger
from mono.utils import ConfigLoader, MonoError


class AgentBuilder:


	def __init__(self) -> None:
		self.configloader = ConfigLoader()

		self.agents: dict[int, Agent] = {}
		self.current_id = 0


	def build(self, filepath: str):

		logger.info("agent", f"Building agent from {filepath}...")

		try:
			self.configloader.load(filepath)
		except MonoError as e:
			logger.critical("agent", f"Failed to load agent file {filepath}: {str(e)}")
			raise

		try:
			name = self.configloader.get("agent.name")
			identity = self.configloader.get("agent.identity")
		except MonoError as e:
			logger.critical("agent", f"Cannot build agent. {str(e)}")
			raise
		
		agent = Agent(
			self.current_id,
			name=name,
			identity=identity
			)

		self.agents[self.current_id] = agent
		self.current_id += 1

		logger.debug("agent", f"Agent({agent.id}) named '{agent.name}' created from {filepath}.")

		context = ContextModule()
		model = ModelModule()

		context.register(agent)
		model.register(agent)

		return agent


		