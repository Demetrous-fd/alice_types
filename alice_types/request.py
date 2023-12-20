from datetime import datetime
from typing import List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field

from alice_types import State, Markup, Meta, Session, NaturalLanguageUnderstanding


class RequestType(str, Enum):
    SIMPLE_UTTERANCE = "SimpleUtterance"
    BUTTON_PRESSED = "ButtonPressed"


class RequestShowType(str, Enum):    
    # https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    SHOW_PULL = "Show.Pull"
    

class ShowType(str, Enum):
    MORNING = "MORNING"


class RequestPurchaseType(str, Enum):    
    # https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
    PURCHASE_CONFIRMATION = "Purchase.Confirmation"


class RequestAudioType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    AUDIO_PLAYER_PLAYBACK_STARTED = "AudioPlayer.PlaybackStarted"
    AUDIO_PLAYER_PLAYBACK_FINISHED = "AudioPlayer.PlaybackFinished"
    AUDIO_PLAYER_PLAYBACK_NEARLY_FINISHED = "AudioPlayer.PlaybackNearlyFinished"
    AUDIO_PLAYER_PLAYBACK_STOPPED = "AudioPlayer.PlaybackStopped"
    AUDIO_PLAYER_PLAYBACK_FAILED = "AudioPlayer.PlaybackStopped"


class RequestAudioErrorType(str, Enum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"
    

class RequestAudioError(BaseModel):
    message: str = Field(...)
    type: RequestAudioErrorType = Field(...)


class RequestSimpleUtterance(BaseModel):
    type: RequestType
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    payload: Optional[dict] = Field(default=None)
    command: Optional[str] = Field(default=None)  # Can be none if payload passed
    original_utterance: Optional[str] = Field(default=None, max_length=1024)  # Can be none if payload passed
    markup: Optional[Markup] = Field(default=None)
    
    def is_ping(self) -> bool:
        return self.original_utterance == "ping"


# https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
class RequestPurchase(BaseModel):
    type: RequestPurchaseType = Field(...)
    purchase_request_id: str = Field(...)
    purchase_token: str = Field(...)
    order_id: str = Field(...)
    purchase_timestamp: datetime = Field(...)
    purchase_payload: dict = Field(...)
    signed_data: str = Field(...)  # TODO: validation
    signature: str = Field(...)
    

class RequestAudio(BaseModel):
    type: RequestAudioType
    error: Optional[RequestAudioError] = Field(default=None)
    
    def has_error(self) -> bool:
        return bool(self.error)
    

class RequestShow(BaseModel):
    type: RequestShowType
    show_type: RequestShowType


class AliceRequest(BaseModel):
    meta: Meta
    request: Union[RequestSimpleUtterance, RequestShow, RequestAudio, RequestPurchase]
    session: Session
    state: State
    version: str
