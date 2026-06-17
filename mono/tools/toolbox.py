from mono.utils import logger

from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True, frozen=True)
class ToolSpec:
	name: str
	info: str
	arguments: dict[str, tuple[type, str]]
	func: Callable[..., ToolResult]


@dataclass(kw_only=True, frozen=True)
class ToolSpace:
	namespace: str
	tools: dict[str, ToolSpec]


@dataclass(frozen=True)
class ToolResult:
	success: bool
	output: str


class ToolBox:
 
	_toolspaces: dict[str, ToolSpace] = {}

	def __init__(self) -> None:
		pass
	

	def get_tool(self, namespace: str, name: str) -> ToolSpec | None:
		space = ToolBox._toolspaces.get(namespace, None)
		if space is None: return

		tool = space.tools.get(name, None)
		if tool is None: return

		return tool 
	

	def get_namespace(self, namespace: str) -> ToolSpace | None:
		space = ToolBox._toolspaces.get(namespace, None)
		return space

	
	def has_namespace(self, name: str) -> bool:
		if name in ToolBox._toolspaces:
			return True
		return False

			
	@classmethod
	def _register(cls, toolspace: ToolSpace):
		if toolspace.namespace in ToolBox._toolspaces:
			logger.warn("tools", f"Toolspace with name '{toolspace.namespace}' was already registered. Ignoring this new one.")
			return
		
		ToolBox._toolspaces[toolspace.namespace] = toolspace
		logger.info("tools", f"Toolspace '{toolspace.namespace}' registered.")

		for tool in toolspace.tools.values():
			logger.debug("tools", f"Added tool: {toolspace.namespace}::{tool.name}")


class ToolRegistry:


	def __init__(self, namespace: str) -> None:
		self._namespace = namespace
		self._tools: dict[str, ToolSpec] = {}


	def submit(self):
		ToolBox._register(
				ToolSpace(
				namespace=self._namespace,
				tools=self._tools
			)
		)


	def tool(
		self,
		name: str,
		info: str,
		arguments: dict[str, tuple[type, str]]
	):
		
		def decorator(func: Callable[..., ToolResult]):

			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)
			

			self._tools[name] = ToolSpec(
				name=name,
				info=info,
				arguments=arguments,
				func=func
			)

			return wrapper
		
		return decorator
	


	
	