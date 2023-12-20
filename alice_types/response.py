from typing import List, Optional, Union

from pydantic import BaseModel, Field

from alice_types import Button, Analytics
from alice_types.cards import BigImage, ImageGallery, ItemsList
from alice_types.directives import AudioPlayerPlay, AudioPlayerStop, StartAccountLinking
    

class Response(BaseModel):
    text: str = Field(..., max_length=1024)
    tts: Optional[str] = Field(default=None, max_length=1024)
    card: Optional[Union[BigImage, ItemsList, ImageGallery]] = Field(default=None)
    buttons: Optional[List[Button]] = Field(default_factory=list)
    end_session: bool = Field(default=False)
    directives: Optional[Union[AudioPlayerPlay, AudioPlayerStop, StartAccountLinking]] = Field(default=None)
    show_item_meta: Optional[dict] = Field(default=None)
    

class AliceResponse(BaseModel):
    response: Response = Field(...)
    session_state: dict
    user_state_update: dict
    application_state: dict
    analytics: Optional[Analytics] = Field(default=None)
    version: str = Field(...)
