from typing import Optional, Union
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4, field_serializer, field_validator

from alice_types.validators import validate_tts_size
from alice_types.response import TextToSpeechModel


class ShowItemMeta(BaseModel):
    content_id: Union[UUID4, str] = Field(
        default_factory=uuid4,
        description="Уникальный идентификатор истории. Формат UUID предпочтителен, но не является обязательным."
    )
    title: Optional[str] = Field(
        default=None,
        description="""
Заголовок истории для экрана, необязательный параметр. 
Если заголовок указан, то на экране покажется:
- сам заголовок истории title с большой буквы;
- перенос строки;
- текст истории из параметра text.        
"""
    )
    title_tts: Optional[str] = Field(
        default=None,
        description="""
Заголовок истории с голосовой разметкой (text-to-speech), необязательный параметр. 
Если заголовок указан, то история в шоу будет составлена из title_tts <пауза 200 мс> text_tts.
"""
    )
    publication_date: datetime = Field(
        default=...,
        description="""
Дата и время создания истории. Алиса игнорирует истории старше 7 дней. 
Строка приводится по UTC в формате ISO 8601: YYYY-MM-DDTHH:mm:ss.sssZ.
"""
    )
    expiration_date: Optional[datetime] = Field(
        default=None,
        description="""
Дата и время, до которого история будет актуальна. 
Алиса не добавит в шоу историю, у которой значение expiration_date раньше, чем время запуска шоу. 
Строка приводится по UTC в формате ISO 8601: YYYY-MM-DDTHH:mm:ss.sssZ.
"""
    )

    @field_serializer("publication_date", "expiration_date")
    def serialize_date(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    #TODO: Узнать максимальный размер title_tts
    validate_tts_size = field_validator("title_tts", mode="before")(
        validate_tts_size
    )


class ShowResponse(TextToSpeechModel):
    """
    Формат ответа аналогичен обычному сообщению от навыка, но имеет особенности:
    - обновление состояния в ответе игнорируется (session_state, user_state_update, application_state);
    - не отображаются кнопки (buttons) и картинки (card).
    """
    show_item_meta: ShowItemMeta = Field(
        default=...,
        description="Параметр историй утреннего шоу Алисы."
    )
