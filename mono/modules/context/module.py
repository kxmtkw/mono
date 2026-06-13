from mono.core.module import Module
from mono.agent.agent import Agent

from .storage import AgentContext, guide

from mono.utils import logger
from mono.utils.error import MonoError


class ContextError(MonoError):
	def __init__(self, msg: str, level: MonoError.ErrorLevel = MonoError.ErrorLevel.medium) -> None:
		super().__init__(msg, level)


class ContextModule(Module):

	_initialized = False

	def __init__(self) -> None:
		super().__init__()
		if self._initialized: return

		self.contexts: dict[int, AgentContext] = {}

		self._initialized = True
		

	def register(self, agent: Agent):
		"Register an agent. If an agent is already present, it would do nothing."

		if agent.id in self.contexts: 
			logger.debug("context", f"Agent({agent.id}) is already registered.")
			return

		self.contexts[agent.id] = AgentContext("", [])
		logger.info("context", f"Registered agent({agent.id}).")


	def unregister(self, agent: Agent):
		"Unregister an agent. Raises ContextError if the agent is not present."

		if agent.id not in self.contexts:
			logger.warn("context", f"Agent({agent.id}) is not registered.")
			raise ContextError("Agent not registered.", MonoError.ErrorLevel.low)
		
		self.contexts.pop(agent.id, None)
		logger.info("context", f"Unregistered agent({agent.id}).")


	def set_system_section(self, agent, *, system: str):
		"Set the system section of an agent. Raises ContextError if agent not registered."

		if agent.id not in self.contexts:
			logger.warn("context", f"Tried updating system section, agent({agent.id}) is not registered.")
			raise ContextError("Agent not registered.")
		
		context = self.contexts[agent.id]
		context.system = system
		logger.debug("context", f"Updated system section of agent({agent.id}).")


	def add_message(self, agent: Agent, *, role: str, mesg: str):
		"Add a message to the agent's chat. Ignores if agent is not registered."

		if agent.id not in self.contexts:
			logger.warn("context", f"Tried adding message, agent({agent.id}) is not registered.")
			return
		
		context = self.contexts[agent.id]
		context.chat.append(f"{role.upper()}: {mesg}")
		logger.debug("context", f"Updated chat of agent({agent.id}) with role '{role}'.")


	def make_prompt(self, agent: Agent, *, role: str, msg: str) -> str:
		"Assemble a prompt. Raises ContextError if agent not registered."

		if agent.id not in self.contexts:
			logger.warn("context", f"Assembling prompt, agent({agent.id}) is not registered.")
			raise ContextError("Agent not registered.", MonoError.ErrorLevel.medium)

		context = self.contexts[agent.id]

	
		prompt = f"{guide}\n[SYSTEM]\n{context.system}\n\n"
		prompt += f"[CHAT]\n{'\n'.join(context.chat)}\n\n"
		prompt += f"[PROMPT]\n{role.upper()}: {msg}"

		logger.info("context", f"Assembling prompt for agent({agent.id}).")

		return prompt
		