from typing import List, Optional, Literal
import locale

from pydantic import BaseModel, Field, field_validator
import pytz

from alice_types.request.interfaces import Interfaces

# TODO: Возможно flags появляется при запуске со станций, надо уточнить
# https://github.com/mahenzon/aioalice/blob/e66615138bf6ae4883154de7fe19a9f8c8c065bc/tests/_dataset.py#L216
POSSIBLE_FLAGS = Literal["no_cards_support"]


class Meta(BaseModel):
    locale: str = Field(..., max_length=64)
    timezone: str = Field(..., max_length=64)
    client_id: str = Field(..., max_length=1024)
    interfaces: Optional[Interfaces] = Field(default=None)
    flags: Optional[List[POSSIBLE_FLAGS]] = Field(default=None)

    @field_validator("timezone", mode="before")  # type: ignore
    @classmethod
    def validate_timezone(cls, value):
        if value not in pytz.all_timezones:
            raise ValueError(f"Timezone: {value} not exists or not valid")
        return value

    @field_validator("locale", mode="before")  # type: ignore
    @classmethod
    def validate_locale(cls, value):
        if value.replace("-", "_").lower() not in locale.locale_alias:
            raise ValueError(f"Locale: {value} not exists or not valid")
        return value
    
