from typing import Union

from pydantic import BaseModel, Field

from alice_types.request.meta import Meta
from alice_types.request.state import State
from alice_types.request.session import Session
from alice_types.request.type.show import RequestShow
from alice_types.request.type.audio import RequestAudio
from alice_types.request.type.purchase import RequestPurchase
from alice_types.request.type.button import RequestButtonPressed
from alice_types.request.type.simple import RequestSimpleUtterance


class AliceRequest(BaseModel):
    meta: Meta = Field(...)
    request: Union[
        RequestButtonPressed,
        RequestSimpleUtterance,
        RequestShow,
        RequestPurchase,
        RequestAudio,
    ] = Field(...)
    session: Session = Field(...)
    state: State = Field(...)
    version: str = Field(...)

    def is_ping(self) -> bool:
        if isinstance(self.request, RequestSimpleUtterance):
            return self.request.is_ping()
        return False
