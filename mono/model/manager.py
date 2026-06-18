from mono.model.response import ModelResponse
from mono.model.base import BaseModelProvider
from mono.utils.logger import Logger
from mono.utils.error import MonoError

from models import MODELS

logger = Logger("model")

class ModelManager():


	def __init__(self) -> None:
		super().__init__()
		self.registered_agents: dict[int, BaseModelProvider] = {}
		self.available_models: dict[str, type[BaseModelProvider]] = {}

		self.loadModels()


	def loadModels(self):

		for model_cls in MODELS:
			self.available_models[model_cls.name()] = model_cls
			logger.debug(f"Found model: {model_cls.name()}")
		

	def register(self, agent: int, model: str):


		if model not in self.available_models:
			logger.critical(f"Unknown model loaded by agent({agent}): {model}")

			raise MonoError(f"Unknown model: {model}", MonoError.ErrorLevel.high)
		
		try:
			self.registered_agents[agent] = self.available_models[model]()
		except MonoError as e:
			logger.critical(f"Error during init of {model} by agent({agent}): {e}")
			raise e
		
		logger.info(f"Registered agent({agent}) using model: {model}.")
	

	def unregister(self, agent: int):

		if agent not in self.registered_agents:
			logger.warn(f"Agent({agent}) is not registered. So can't unregister.")
			return 
				
		self.registered_agents.pop(agent)

		logger.info(f"Unregistered agent({agent}).")


	def ask(self, agent: int, request: str) -> ModelResponse:
		
		# we expect agent to be a registered agent
		# if this call is made then something went wrong
		model = self.registered_agents[agent]

		try:
			logger.info(f"Made model request. Triggered by agent({agent}).")
			response = model.ask(request)
			return response
		
		except MonoError as e:
			logger.critical(f"Model({model.name()}) call by agent({agent}) failed: {e.msg}")
			raise MonoError(f"Model({model.name()}) call by agent({agent}) failed: {e.msg}", e.level)