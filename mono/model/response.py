from pydantic import BaseModel, ConfigDict
from typing import Any, List, Literal, Optional


class ToolArgument(BaseModel):
	name: str
	value: str


class ToolCall(BaseModel):
	namespace: str
	toolname: str
	args: list[ToolArgument]


class ModelResponse(BaseModel):
	response: str
	toolcall: ToolCall | list[ToolCall] | None
	
	@classmethod
	def convert_to_dict(cls, tool_args: list[Any]) -> dict[str, Any]:
		return {arg.name: arg.value for arg in tool_args}

