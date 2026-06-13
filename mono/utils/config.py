import tomllib
from typing import Any, Optional, List
from mono.utils.error import MonoError


class ConfigLoader:
	
	def __init__(self) -> None:
		self._config: dict[str, Any] = {}


	def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '.') -> dict:
		items = []
		for k, v in d.items():
			new_key = f"{parent_key}{sep}{k}" if parent_key else k
			if isinstance(v, dict):
				items.extend(self._flatten_dict(v, new_key, sep=sep).items())
			else:
				items.append((new_key, v))
		return dict(items)


	def load(self, filepath: str) -> None:
		try:
			with open(filepath, "rb") as f:
				data = tomllib.load(f)
				self._config = self._flatten_dict(data)
		except Exception as e:
			raise MonoError(f"Failed to load config file {filepath}: {e}")


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
