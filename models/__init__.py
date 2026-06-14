from .gemma import Gemma26B
from .gemini import GeminiFlashLite

from mono.model.base import BaseModelProvider

MODELS: list[type[BaseModelProvider]] = [
	Gemma26B,
	GeminiFlashLite
]