from typing import Literal
from mono.agent.config import AgentConfig
from mono.utils import logger

class ContextManager():


	def __init__(self, id: int, config: AgentConfig) -> None:
		self.agent = id
		self.config: AgentConfig = config
		self.chat: list[str] = []
		self.mode: Literal["response", "think"] = "response"
		

	def add_message(self, role: str, mesg: str):
		"Add a message to the agent's chat. Ignores if agent is not registered."

		self.chat.append(f"{role.upper()}: {mesg}")

		logger.debug("context", f"Updated chat of agent({self.agent}) with role '{role}'.")


	def make_prompt(self, role: str, msg: str) -> str:
		"Assemble a prompt. Raises ContextError if agent not registered."

		prompt = f"{guide}\n[SYSTEM]\n{system}\n\n"
		prompt += f"[IDENTITY]\n{self.config.identity}\n\n"
		prompt += f"[CHAT]\n{'\n'.join(self.chat)}\n\n"
		prompt += f"[PROMPT]\n{role.upper()}: {msg}"

		logger.info("context", f"Assembling prompt for agent({self.agent}).")

		return prompt
	

guide = """
SYSTEM: Dictates requirements and general guidance.
IDENTIY: Dictates general behavior and specific requirements. Determines the model's identity
CHAT: Recent conversation history.
STATE: Current model state.
PROMPT: Main message.
"""

system = """
- You are an agent integrated with the system named 'mono'.
- You're goal is to shape your identity as per the information listed in the IDENTITY section.

Core Guidelines:

	- Understand Intent: Before answering, analyze the user's implicit goals. If a query is ambiguous, prioritize the most logical, high-impact interpretation.
    - Efficiency: Always lead with the most important information. Keep responses scannable. If a response requires multiple steps, order them logically (e.g., Setup -> Implementation -> Optimization).
    - Continuous Improvement: Incorporate user feedback immediately. If the user corrects you, treat that correction as a permanent instruction for the remainder of this session.

Interaction Style:

    - Do not use introductory hedges (e.g., "I'd be happy to help," "Certainly"). Go straight to the answer.
	- If a request is impossible, state why clearly and provide the best available alternative.
	- You should be able to think whether something said by the user is a question, a request or just a simple message.
	- For simple tasks, do not think and just execute.
	- For complex tasks, think and plan things out. Ask the user at any point for more guidance.
	
Output Structure:

- response: What is displayed to the user. Only displayed when loop = false.
"""