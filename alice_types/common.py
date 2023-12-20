from typing import Optional

from pydantic import BaseModel, Field


class Text(BaseModel):
    value: str = Field(...)
    tts: Optional[str] = Field(default=None)


# class Image(BaseModel):
    
