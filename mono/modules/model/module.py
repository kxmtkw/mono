from mono.core.module import Module
from mono.agent.agent import Agent

from google import genai

from mono.utils import logger
from mono.utils.error import MonoError


class ModelError(MonoError):
	def __init__(self, msg: str, level: MonoError.ErrorLevel = MonoError.ErrorLevel.medium) -> None:
		super().__init__(msg, level)


class ModelModule(Module):

	_initialized = False

	def __init__(self) -> None:
		super().__init__()
		if self._initialized: return

		self.registered_agents: set[int] = set()
		self.client = genai.Client(api_key="AQ.Ab8RN6I-HkghglylNFMRWUVVAZ9tB9eWig-TLr976ELEiXqrBA")

		self._initialized = True


	def register(self, agent: Agent):
		"Register an agent. If an agent is already present, it would do nothing."
		self.registered_agents.add(agent.id)
		logger.info("model", f"Registered agent({agent.id}).")
	

	def unregister(self, agent: Agent):
		"Unregister an agent. Raises ModelError if agent is not registered."

		if agent.id not in self.registered_agents:
			logger.warn("model", f"Agent({agent.id}) is not registered.")
			raise MonoError("Agent not registered.", MonoError.ErrorLevel.low)
		
		self.registered_agents.remove(agent.id)
		logger.info("model", f"Unregistered agent({agent.id}).")


	def ask(self, agent: Agent, *, request: str) -> str:
		"Make a model request. Raises ModelError if agent is not registered (low) or model call fails (high)."

		if agent.id not in self.registered_agents:
			logger.warn("model", f"Agent({agent.id}) is not registered.")
			raise ModelError("Agent not registered.")

		try:
			response = self.client.models.generate_content(
				model="gemini-3.1-flash-lite",
				contents=request,
			)
			logger.info("model", f"Made model request. Triggered by agent({agent.id}).")

			if response.text:
				return response.text
			else:
				raise ModelError("Response is empty.")
			
		except Exception as e:
			logger.critical("model", f"API call failed: {str(e)}")
			raise ModelError(f"Model call failure: {str(e)}", ModelError.ErrorLevel.medium)