from pydantic import BaseModel
from typing import List, Literal, Optional

class ModelResponse(BaseModel):
	response: str