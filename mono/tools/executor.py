from dataclasses import dataclass

class ToolCall:
	pass

@dataclass(frozen=True)
class ToolResult:
	success: bool
	output: str