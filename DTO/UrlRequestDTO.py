from pydantic import BaseModel

class UrlRequestDTO(BaseModel):
    url: str
    lang_from: str = None
    lang_to: str = None