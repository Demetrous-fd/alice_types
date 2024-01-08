from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator

from alice_types import Button
from alice_types.mixin import ExcludeUnsetMixin
from alice_types.validators import validate_tts_size
from alice_types.cards import BigImage, ImageGallery, ItemsList
from alice_types.directives import AudioPlayerPlay, AudioPlayerStop, StartAccountLinking


class TextToSpeechModel(BaseModel, ExcludeUnsetMixin):
    text: str = Field(
        default="",
        max_length=1024,
        description="Текст, который следует показать и озвучить пользователю. Может быть пустым, если заполнено свойство tts."
    )
    tts: Optional[str] = Field(
        default=None,
        exclude_unset=True,
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
    ]] = Field(default=None, exclude_unset=True)
    buttons: Optional[List[Button]] = Field(default_factory=list, exclude_unset=True)
    end_session: bool = Field(default=False)
    directives: Optional[Union[
        AudioPlayerPlay,
        AudioPlayerStop,
        StartAccountLinking
    ]] = Field(default=None, exclude_unset=True)
