from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl, field_validator

from alice_types.validators import validate_dict_size
from alice_types.mixin import ExcludeUnsetMixin


class Button(BaseModel, ExcludeUnsetMixin):
    title: Optional[str] = Field(
        default="",
        max_length=64,
        description="Если для кнопки не указано свойство url, по нажатию текст кнопки будет отправлен навыку как реплика пользователя."
    )
    url: Optional[AnyHttpUrl] = Field(default=None, max_length=1024, exclude_unset=True)
    payload: dict = Field(default_factory=dict, exclude_unset=True)
    hide: bool = Field(default=False, exclude_unset=True)

    validate_payload_size = field_validator("payload", mode="before")(
        validate_dict_size(max_size=4094)
    )
