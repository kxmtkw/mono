from dataclasses import dataclass
from pydantic import BaseModel


class AgentIdentity(BaseModel):
	name: str
	intro: str
	personality: str
	behavior: str
	constraints: str


class AgentCapabilities(BaseModel):
	allowed_tools: list[str]


class AgentModel(BaseModel):
	mutable: bool
	provider: str
	name: str


class AgentConfig(BaseModel):
	identity: AgentIdentity
	capabilities: AgentCapabilities
	model: AgentModel
	
