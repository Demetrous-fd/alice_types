from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator

from alice_types.request import Markup, NaturalLanguageUnderstanding
from alice_types.validators import validate_dict_size


class RequestButtonPressed(BaseModel):
    markup: Optional[Markup] = Field(default=None)
    nlu: Optional[NaturalLanguageUnderstanding] = Field(default=None)
    payload: Optional[dict] = Field(default=None)
    type: Literal["ButtonPressed"] = Field(...)

    validate_payload_size = field_validator("payload", mode="before")(
        validate_dict_size(max_size=4094)
    )
