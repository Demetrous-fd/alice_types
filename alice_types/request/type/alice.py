from typing import Union, Optional

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
    request: Optional[
        Union[
            RequestButtonPressed,
            RequestSimpleUtterance,
            RequestShow,
            RequestPurchase,
            RequestAudio,
        ]
    ] = Field(default=None)
    session: Session = Field(...)
    state: State = Field(...)
    version: str = Field(...)
    account_linking_complete_event: Optional[dict] = Field(default=None)

    def is_ping(self) -> bool:
        if self.request is None:
            return False

        if isinstance(self.request, RequestSimpleUtterance):
            return self.request.is_ping()
        return False

    def is_new_session(self) -> bool:
        return self.session.new

    def authorization_is_completed(self) -> bool:
        return self.account_linking_complete_event is not None
