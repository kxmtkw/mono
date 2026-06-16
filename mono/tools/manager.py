
from mono.utils import MonoError, logger
from .toolbox import ToolBox, ToolSpace
from .executor import ToolResult


class ToolManager:

	def __init__(self) -> None:
		self.registered_agents: dict[int, set[str]] = {}
		self.toolbox = ToolBox()


	def register(self, agent_id: int, capabilities: list[str]):

		for c in capabilities:
			if not self.toolbox.has_namespace(c):
				raise MonoError(f"Unknown capability: {c}", MonoError.ErrorLevel.medium)

		self.registered_agents[agent_id] = set(capabilities)

		logger.info("tools", f"Registered agent({agent_id}) with capabilities: {capabilities}")

	
	def unregister(self, agent_id: int):

		if agent_id not in self.registered_agents:
			logger.warn("tools", f"Agent({agent_id}) is not registered. So can't unregister.")
			return 
				
		self.registered_agents.pop(agent_id)

		logger.info("tools", f"Unregistered agent({agent_id}).")


	def get_agent_toolbox(self, agent_id: int) -> list[ToolSpace]:

		if agent_id not in self.registered_agents:
			logger.warn("tools", f"Agent({agent_id}) is not registered. Can't give toolbox to caller.")
			return []
		
		spaces = []

		for c in self.registered_agents[agent_id]:
			space = self.toolbox.get_namespace(c)
			if space: spaces.append(space) # space always exists because if the agent was registered. error would have been raised.

		return spaces


	def execute(self, agent_id: int, space: str, name: str, args: dict[str, str]) -> ToolResult:

		logger.info("tools", f"Agent({agent_id}) executed tool: {space}::{name}")

		tool = self.toolbox.get_tool(space, name)

		if not tool:
			raise MonoError(f"Unknown tool executed: {space}::{name}", MonoError.ErrorLevel.medium)

		if space not in self.registered_agents[agent_id]:
			raise MonoError(f"Agent({agent_id}) does'nt have the capability to execute {space}::{name}", MonoError.ErrorLevel.high)
		
		try:
			result = tool.func(**args)
		except Exception as e:
			msg =  f"Tool {space}::{name} failed. {e.__class__.__name__}: {e}. Should not have happened."
			logger.critical("tools", msg)
			return ToolResult(
				False,
			 	msg
			)
		
		logger.debug("tools", f"Tool {space}::{name} result: Success({result.success})")

		return result

		


		