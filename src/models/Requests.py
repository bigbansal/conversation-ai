from pydantic import BaseModel

class TextPromptRequest(BaseModel):
    prompt: str