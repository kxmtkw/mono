from google import genai

from mono.model.response import ModelResponse
from mono.model.base import BaseModelProvider
from mono.utils import logger
from mono.utils.error import MonoError


from models import MODELS

class ModelManager():


	def __init__(self) -> None:
		super().__init__()
		self.registered_agents: dict[int, str] = {}
		self.loaded_models: dict[str, BaseModelProvider] = {}

		self.loadModels()


	def loadModels(self):

		for model_cls in MODELS:
			model = model_cls()
			model.start()
			self.loaded_models[model.name()] = model
			logger.debug("model", f"Loaded model: {model.name()}")
		

	def register(self, agent: int, model: str):
		"Register an agent. If an agent is already present, it would update the model field."

		if model not in self.loaded_models:
			logger.critical("model", f"Unknown model: {model}")
			raise MonoError(f"Unknown model: {model}", MonoError.ErrorLevel.high)
		
		self.registered_agents[agent] = model
		logger.info("model", f"Registered agent({agent}) using model: {model}.")
	

	def unregister(self, agent: int):
		"Unregister an agent. Raises MonoError if agent is not registered."

		if agent not in self.registered_agents:
			logger.warn("model", f"Agent({agent}) is not registered.")
			raise MonoError("Agent not registered.", MonoError.ErrorLevel.low)
		
		self.registered_agents.pop(agent)
		logger.info("model", f"Unregistered agent({agent}).")


	def ask(self, agent: int, *, request: str) -> ModelResponse:
		"Make a model request. Raises MonoError if agent is not registered (low) or model call fails (high)."

		if agent not in self.registered_agents:
			logger.warn("model", f"Agent({agent}) is not registered.")
			raise MonoError("Agent not registered.")

		model_name = self.registered_agents[agent]
		model = self.loaded_models[model_name]

		try:
			response = model.ask(request)

			logger.info("model", f"Made model request. Triggered by agent({agent}).")

			return response
		
		except Exception as e:
			logger.critical("model", f"API call failed: {str(e)}")
			raise MonoError(f"Model call failure: {str(e)}", MonoError.ErrorLevel.medium)