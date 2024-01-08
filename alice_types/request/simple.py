from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator

from alice_types import Markup, NaturalLanguageUnderstanding
from alice_types.validators import validate_dict_size


class RequestSimpleUtterance(BaseModel):
    command: Optional[str] = Field(default=None)  # Can be none if payload passed
    original_utterance: Optional[str] = Field(default=None, max_length=1024)  # Can be none if payload passed
    markup: Optional[Markup] = Field(default=None)
    payload: Optional[dict] = Field(default=None)
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    type: Literal["SimpleUtterance"] = Field(...)

    validate_payload_size = field_validator("payload", mode="before")(
        validate_dict_size(max_size=4094)
    )

    def is_ping(self) -> bool:
        return self.original_utterance == "ping"
