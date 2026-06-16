from pydantic import BaseModel, ConfigDict
from typing import Any, List, Literal, Optional

class ToolArgument(BaseModel):
	name: str
	value: str

class ModelResponse(BaseModel):
	response: str
	tool_called: bool
	tool_namespace: str
	tool_func_name: str
	tool_args: list[ToolArgument]
	
	@classmethod
	def convert_to_dict(cls, tool_args: list[Any]) -> dict[str, Any]:
		return {arg.name: arg.value for arg in tool_args}

