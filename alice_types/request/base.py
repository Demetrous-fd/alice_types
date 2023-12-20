from typing import Optional, Union
from enum import Enum

from pydantic import BaseModel, Field

from alice_types import State, Markup, Meta, Session, NaturalLanguageUnderstanding
from alice_types.request import RequestAudio, RequestPurchase, RequestShow


class RequestType(str, Enum):
    SIMPLE_UTTERANCE = "SimpleUtterance"
    BUTTON_PRESSED = "ButtonPressed"


class RequestSimpleUtterance(BaseModel):
    type: RequestType
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    payload: Optional[dict] = Field(default=None)
    command: Optional[str] = Field(default=None)  # Can be none if payload passed
    original_utterance: Optional[str] = Field(default=None, max_length=1024)  # Can be none if payload passed
    markup: Optional[Markup] = Field(default=None)

    def is_ping(self) -> bool:
        return self.original_utterance == "ping"


class AliceRequest(BaseModel):
    meta: Meta
    request: Union[RequestSimpleUtterance, RequestShow, RequestAudio, RequestPurchase]
    session: Session
    state: State
    version: str
