from mono.agent.agent import Agent

from abc import ABC, abstractmethod

class Module(ABC):
	
	_instances = {}

	def __new__(cls, *args, **kwargs):

		if not cls._instances.get(cls, None):
			cls._instances[cls] = super(Module, cls).__new__(cls)
			
		return cls._instances[cls]
	

	def __init__(self) -> None:
		super().__init__()
	

	@abstractmethod
	def register(self, agent: Agent):
		pass
	
	@abstractmethod
	def unregister(self, agent: Agent):
		pass