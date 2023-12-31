from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl
import orjson

from alice_types.mixin import CheckPayloadMixin


class BaseButton(BaseModel, CheckPayloadMixin):
    title: str = Field(
        ..., 
        max_length=64, 
        description="Если для кнопки не указано свойство url, по нажатию текст кнопки будет отправлен навыку как реплика пользователя."
    )
    url: Optional[AnyHttpUrl] = Field(default=None, max_length=1024)
    payload: dict = Field(default_factory=dict)


class Button(BaseButton):
    hide: bool = Field(default=False)
