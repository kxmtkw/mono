from dataclasses import dataclass

class ToolCall:
	pass

@dataclass(frozen=True)
class ToolResult:
	succes: bool
	output: str