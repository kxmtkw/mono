from pathlib import Path

from mono.interface.base import BaseInterface

from mono.agent.agent import Agent
from mono.agent.config import AgentConfig

from mono.model.manager import ModelManager
from mono.tools.manager import ToolManager

from mono.utils import ConfigLoader, MonoError, Logger

logger = Logger("builder")


class AgentBuilder:

	def __init__(
		self,
		model: ModelManager,
		tools: ToolManager
		) -> None:

		self.model = model
		self.tools = tools

		self.configloader = ConfigLoader()

		self.agents: dict[int, Agent] = {}
		self.current_id = 0

		try:
			with open(Path("prompt/system.md")) as file:
				self.system_prompt: str = file.read()
		except FileNotFoundError:
			logger.critical(f"Could not find system.md")
			raise MonoError("Could not file system.md", MonoError.ErrorLevel.high)



	def build(self, filepath: str, iface: BaseInterface):

		logger.info(f"Building agent from {filepath}")

		try:
			self.configloader.load(filepath)
		except MonoError as e:
			logger.critical(f"Failed to load agent file {filepath}: {str(e)}")
			raise

		try:
			data = self.configloader.getdata()
			config = AgentConfig.model_validate(data)
		except Exception as e:
			logger.critical(f"Cannot build agent: {str(e)}")
			raise MonoError(str(e), MonoError.ErrorLevel.high)
		
		agent = Agent(
			id=self.current_id,
			config=config,
			system=self.system_prompt,
			modelmanager=self.model,
			toolmanager=self.tools,
			interface=iface,
		)

		self.agents[self.current_id] = agent
		self.current_id += 1

		logger.info(f"Agent({agent.id}) named '{agent.config.identity.name}' created from {filepath}.")
		
		return agent


		