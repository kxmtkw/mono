from dataclasses import dataclass

@dataclass
class AgentContext:
	system: str
	chat: list[str]

guide = """
SYSTEM: Dictates model behaviour.
CHAT: Recent conversation history.
PROMPT: Main message.
"""