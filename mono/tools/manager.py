
from mono.utils import MonoError, logger
from .toolbox import ToolBox

class ToolManager:

	def __init__(self) -> None:
		self.registered_agents: set[int] = set()
		self.toolbox = ToolBox()


	def register(self, agent: int, model: str):
		self.registered_agents.add(agent)

		logger.info("tools", f"Registered agent({agent}) using model: {model}.")
	

	def unregister(self, agent: int):

		if agent not in self.registered_agents:
			logger.warn("tools", f"Agent({agent}) is not registered. So can't unregister.")
			return 
				
		self.registered_agents.remove(agent)

		logger.info("tools", f"Unregistered agent({agent}).")


	def execute(self, space: str, name: str, args: dict[str, str]):
		logger.info("tools", f"Executing tool: {name}")

		try:
			tool = self.toolbox.get_tool(space, name)
			result = tool.func(**args)
		except Exception as e:
			raise MonoError(str(e), MonoError.ErrorLevel.medium)
		
		logger.debug("tools", f"Tool Result: Success({result.succes})")

		print(result.output)
		


		