from pydantic import BaseModel
from typing import List, Literal, Optional

class ModelResponse(BaseModel):
	response: Optional[str]
	thought: Optional[str]
	mode: Literal["respond", "think"]