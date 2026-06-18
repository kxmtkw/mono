from mono.model.base import BaseModelProvider
from mono.model.response import ModelResponse

from google import genai

from mono.utils.error import MonoError

import os


class Gemma26B(BaseModelProvider):

	model_name: str = "gemma-4-26b-a4b-it"

	def __init__(self) -> None:
		
		
		self.api_key: str | None = os.getenv("GEMINI_API_KEY")

		if not self.api_key:
			raise MonoError(f"API key not found for {self.model_name}. Set the env var: GEMINI_API_KEY")
		
		self.client = genai.Client(
			api_key=self.api_key,
			http_options=genai.types.HttpOptions(timeout=10000)
		)

	
	@classmethod
	def name(cls) -> str:
		return cls.model_name


	def ask(self, msg: str) -> ModelResponse:

		try:
			response = self.client.models.generate_content(
				model=self.model_name,
				contents=msg,
				config=genai.types.GenerateContentConfig(
					response_mime_type="application/json", 
					response_schema=ModelResponse.model_json_schema()
				)
			)

			if response.text:
				return ModelResponse.model_validate_json(response.text)
			else:
				raise MonoError("Response is empty.")
			
		except Exception as e:
			raise MonoError(f"{self.model_name} {e.__class__.__name__} {str(e)}", MonoError.ErrorLevel.medium)