from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from alice_types.response import Button
from alice_types.mixin import ExcludeUnsetMixin
from alice_types.validators import validate_tts_size
from alice_types.response.cards import BigImage, ImageGallery, ItemsList
from alice_types.response.directives import Directives


class TextToSpeechModel(BaseModel, ExcludeUnsetMixin):
    text: str = Field(
        default="",
        max_length=1024,
        description="Текст, который следует показать и озвучить пользователю. Может быть пустым, если заполнено свойство tts."
    )
    tts: Optional[str] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="""
Ответ в формате TTS (text-to-speech). Максимум 1024 символа.
Теги <speaker>, которые используются для ссылок на звуки, не учитываются в ограничении в 1024 символа на длину значения свойства tts.
"""
    )

    validate_tts_size = field_validator("tts", mode="before")(
        validate_tts_size
    )


class Response(TextToSpeechModel):
    card: Optional[Union[
        BigImage,
        ItemsList,
        ImageGallery
    ]] = Field(default=None, json_schema_extra={"exclude_unset": True})
    buttons: Optional[List[Button]] = Field(default_factory=list, json_schema_extra={"exclude_unset": True})
    end_session: bool = Field(default=False, json_schema_extra={"exclude_unset": True})
    directives: Optional[Directives] = Field(default=None, json_schema_extra={"exclude_unset": True})
