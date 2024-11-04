from typing import List
from pydantic import BaseModel

class NllbRequestDTO(BaseModel):
    lang_to: str
    content: List[str]