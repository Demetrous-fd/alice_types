from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl, field_validator

from alice_types.validators import validate_dict_size


class BaseButton(BaseModel):
    title: str = Field(
        ..., 
        max_length=64, 
        description="Если для кнопки не указано свойство url, по нажатию текст кнопки будет отправлен навыку как реплика пользователя."
    )
    url: Optional[AnyHttpUrl] = Field(default=None, max_length=1024)
    payload: dict = Field(default_factory=dict)

    validate_payload_size = field_validator("payload", mode="before")(
        validate_dict_size(max_size=4094)
    )


class Button(BaseButton):
    hide: bool = Field(default=False)
