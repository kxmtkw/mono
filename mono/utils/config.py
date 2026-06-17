import tomllib
from typing import Any, Optional, List
from mono.utils.error import MonoError


class ConfigLoader:
	
	def __init__(self) -> None:
		self._config: dict[str, Any] = {}



	def load(self, filepath: str) -> None:
		try:
			with open(filepath, "rb") as f:
				data = tomllib.load(f)
				self._config = data
		except Exception as e:
			raise MonoError(f"Failed to load config file {filepath}: {e}")
	

	def getdata(self) -> dict[str, Any]:
		return self._config
	

	def get(
		self,
		key: str,
		default: Any = None,
		*,
		required_type: Optional[type] = None,
		required_values: Optional[List[Any]] = None,
	) -> Any:
		
		if key not in self._config:
			if default is not None:
				return default
			raise MonoError(f"Configuration key '{key}' not found.")

		value = self._config[key]

		if required_type is not None and not isinstance(value, required_type):
			raise MonoError(
				f"Configuration key '{key}' must be of type {required_type.__name__}, got {type(value).__name__}."
			)

		if required_values is not None and value not in required_values:
			raise MonoError(
				f"Configuration key '{key}' must be one of {required_values}, got {value}."
			)

		return value
