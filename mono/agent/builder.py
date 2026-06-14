from pathlib import Path

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
		self.system_prompt: str = self.load_system_prompt()

		self.configloader = ConfigLoader()

		self.agents: dict[int, Agent] = {}
		self.current_id = 0


	def load_system_prompt(self) -> str:
		try:
			with open(Path("prompt/system.md")) as file:
				return file.read()
		except FileNotFoundError:
			logger.warn("agent", f"Could not find system.md")
			raise MonoError("Could not file system.md", MonoError.ErrorLevel.high)


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
			persona = self.configloader.get("agent.personality")
			behavior = self.configloader.get("agent.behavior")
			model = self.configloader.get("agent.model")
		except MonoError as e:
			logger.critical("agent", f"Cannot build agent. {str(e)}")
			raise MonoError(e.msg, MonoError.ErrorLevel.high)
		
		agent = Agent(
			self.current_id,
			config= AgentConfig(
				name=name, 
				identity=identity,
				personality=persona,
				behaviour=behavior,
				model=model
			),
			system_prompt=self.system_prompt,
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


		