from pydantic import BaseModel

class AudioRequestDTO(BaseModel):
    lang_from: str = None
    lang_to: str = None