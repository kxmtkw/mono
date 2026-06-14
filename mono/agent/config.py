from dataclasses import dataclass

@dataclass(kw_only=True, frozen=True)
class AgentConfig:
	name: str
	identity: str
	behaviour: dict[str, str]
	model: str
	