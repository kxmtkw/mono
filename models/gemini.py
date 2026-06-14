from mono.model.base import BaseModelProvider
from mono.model.response import ModelResponse

from google import genai

from mono.utils.error import MonoError


class GeminiFlashLite(BaseModelProvider):

	def __init__(self) -> None:
		self.model_name: str = "gemini-3.1-flash-lite"
		self.client = genai.Client(
			http_options=genai.types.HttpOptions(timeout=10)
		)

	
	def name(self) -> str:
		return self.model_name


	def start(self):
		pass


	def end(self):
		pass


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
			raise MonoError(f"{self.model_name} {str(e)}", MonoError.ErrorLevel.medium)