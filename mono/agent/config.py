from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class AgentConfig:
	name: str
	identity: str
	personality: str
	behaviour: str
	model: str
	capabilities: list[str]