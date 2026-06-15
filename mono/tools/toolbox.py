from mono.utils import logger

from dataclasses import dataclass
from typing import Callable

from .executor import ToolResult


@dataclass(kw_only=True, frozen=True)
class ToolSpec:
	name: str
	info: str
	arguments: dict[str, str]
	func: Callable[..., ToolResult]


@dataclass(kw_only=True)
class ToolSpace:
	namespace: str
	tools: dict[str, ToolSpec]


class ToolBox:

	_instance = None
 
	_toolspaces: dict[str, ToolSpace] = {}

	def __new__(cls, *args, **kwargs):
			if cls._instance is None:
				cls._instance = super(ToolBox, cls).__new__(cls)
			return cls._instance
	
	def __init__(self, namespace: str | None = None) -> None:
		if namespace is None: return
		
		self.namespace = namespace
		if namespace not in self._toolspaces:
			self._toolspaces[namespace] = ToolSpace(namespace=namespace, tools={})

	def tool(
		self,
		name: str,
		info: str,
		arguments: dict[str, str]
	):
		
		def decorator(func: Callable[..., ToolResult]):

			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)
			

			ToolBox._toolspaces[self.namespace].tools[name] = ToolSpec(
				name=name,
				info=info,
				arguments=arguments,
				func=func
			)

			logger.debug("tools", f"Added tool: {self.namespace}::{name}")

			return wrapper
		
		return decorator
	

	def get_tool(self, namespace: str, name: str):
		return ToolBox._toolspaces[namespace].tools[name]
			

	