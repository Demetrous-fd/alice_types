from typing import Optional

from pydantic import BaseModel, Field, AnyHttpUrl, field_validator
import orjson


class BaseButton(BaseModel):
    title: str = Field(
        ..., 
        max_length=64, 
        description="Если для кнопки не указано свойство url, по нажатию текст кнопки будет отправлен навыку как реплика пользователя."
    )
    url: Optional[AnyHttpUrl] = Field(default=None, max_length=1024)
    payload: dict = Field(default_factory=dict)
    
    @field_validator("payload", mode="before")
    @classmethod
    def validate_payload(cls, value):
        if isinstance(value, dict):
            data = orjson.dumps(value)
            if len(data) > 4096:
                raise ValueError(f"Payload is big; Max bytes size: 4096; Current size: {len(data)}")
        return value


class Button(BaseButton):
    hide: bool = Field(default=False)

