from google import genai

from mono.model.response import ModelResponse
from mono.utils import logger
from mono.utils.error import MonoError


class ModelError(MonoError):
	def __init__(self, msg: str, level: MonoError.ErrorLevel = MonoError.ErrorLevel.medium) -> None:
		super().__init__(msg, level)


class ModelManager():


	def __init__(self) -> None:
		super().__init__()
		self.registered_agents: set[int] = set()
		self.client = genai.Client(api_key="")


	def register(self, agent: int):
		"Register an agent. If an agent is already present, it would do nothing."
		self.registered_agents.add(agent)
		logger.info("model", f"Registered agent({agent}).")
	

	def unregister(self, agent: int):
		"Unregister an agent. Raises ModelError if agent is not registered."

		if agent not in self.registered_agents:
			logger.warn("model", f"Agent({agent}) is not registered.")
			raise MonoError("Agent not registered.", MonoError.ErrorLevel.low)
		
		self.registered_agents.remove(agent)
		logger.info("model", f"Unregistered agent({agent}).")


	def ask(self, agent: int, *, request: str) -> ModelResponse:
		"Make a model request. Raises ModelError if agent is not registered (low) or model call fails (high)."

		if agent not in self.registered_agents:
			logger.warn("model", f"Agent({agent}) is not registered.")
			raise ModelError("Agent not registered.")

		
		try:
			response = self.client.models.generate_content(
				model="gemini-3.1-flash-lite",
				contents=request,
				config=genai.types.GenerateContentConfig(
					response_mime_type="application/json", 
					response_schema=ModelResponse.model_json_schema()
				)
			)

			logger.info("model", f"Made model request. Triggered by agent({agent}).")

			if response.text:
				return ModelResponse.model_validate_json(response.text)
			else:
				raise ModelError("Response is empty.")
			
		except Exception as e:
			logger.critical("model", f"API call failed: {str(e)}")
			raise ModelError(f"Model call failure: {str(e)}", ModelError.ErrorLevel.medium)