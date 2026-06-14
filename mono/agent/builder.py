
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
		except MonoError as e:
			logger.critical("agent", f"Cannot build agent. {str(e)}")
			raise
		
		agent = Agent(
			self.current_id,
			self.model,
			ContextManager(self.current_id, identity),
			iface,
			name=name,
			identity=identity,
			model=""
			)

		self.agents[self.current_id] = agent
		self.current_id += 1

		logger.debug("agent", f"Agent({agent.id}) named '{agent.name}' created from {filepath}.")

		self.model.register(agent.id)

		return agent


		