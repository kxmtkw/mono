
from mono.agent.config import AgentConfig
from mono.interface.base import BaseInterface

from .agent import Agent
from .context import ContextManager

from mono.model.manager import ModelManager
from mono.utils import logger
from mono.utils import ConfigLoader, MonoError


class AgentBuilder:

	def __init__(
		self,
		model: ModelManager
		) -> None:
		self.model = model

		self.configloader = ConfigLoader()

		self.agents: dict[int, Agent] = {}
		self.current_id = 0


	def build(self, filepath: str, iface: BaseInterface):

		logger.info("agent", f"Building agent from {filepath}...")

		try:
			self.configloader.load(filepath)
		except MonoError as e:
			logger.critical("agent", f"Failed to load agent file {filepath}: {str(e)}")
			raise

		try:
			name = self.configloader.get("agent.name")
			identity = self.configloader.get("agent.identity")
			behavior = self.configloader.get("agent.behavior")
			model = self.configloader.get("agent.model")
		except MonoError as e:
			logger.critical("agent", f"Cannot build agent. {str(e)}")
			raise
		
		agent = Agent(
			self.current_id,
			config= AgentConfig(
				name=name, 
				identity=identity,
				behaviour=behavior,
				model=model
			),
			model_manager=self.model,
			interface=iface,
		)

		self.agents[self.current_id] = agent
		self.current_id += 1

		logger.debug("agent", f"Agent({agent.id}) named '{agent.config.name}' created from {filepath}.")

		try:
			self.model.register(agent.id, agent.config.model)
		except MonoError as e:
			logger.critical("agent", f"Cannot build agent. {str(e)}")
			raise
		
		return agent


		