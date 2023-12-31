from typing import Optional, Union, Literal
from enum import Enum

from pydantic import BaseModel, Field

from alice_types import State, Markup, Meta, Session, NaturalLanguageUnderstanding
from alice_types.request import RequestAudio, RequestPurchase, RequestShow
from alice_types.mixin import CheckPayloadMixin


class RequestType(str, Enum):
    SIMPLE_UTTERANCE = "SimpleUtterance"
    BUTTON_PRESSED = "ButtonPressed"


# TODO: Посмотреть ответы от Алисы
class RequestButtonPressed(BaseModel, CheckPayloadMixin):
    type: Literal[RequestType.BUTTON_PRESSED] = Field(...)
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    payload: Optional[dict] = Field(default=None)


class RequestSimpleUtterance(BaseModel, CheckPayloadMixin):
    command: Optional[str] = Field(default=None)  # Can be none if payload passed
    original_utterance: Optional[str] = Field(default=None, max_length=1024)  # Can be none if payload passed
    markup: Optional[Markup] = Field(default=None)
    payload: Optional[dict] = Field(default=None)
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    type: Literal[RequestType.SIMPLE_UTTERANCE] = Field(...)

    def is_ping(self) -> bool:
        return self.original_utterance == "ping"


class AliceRequest(BaseModel):
    meta: Meta = Field(...)
    request: Union[RequestButtonPressed, RequestSimpleUtterance, RequestShow, RequestAudio, RequestPurchase] = Field(...)
    session: Session = Field(...)
    state: State = Field(...)
    version: str = Field(...)
