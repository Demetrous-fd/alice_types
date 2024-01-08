from typing import Union

from pydantic import BaseModel, Field

from alice_types.request import (
    RequestAudio,
    RequestPurchase,
    RequestShow,
    RequestSimpleUtterance,
    RequestButtonPressed
)
from alice_types import State, Meta, Session


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
