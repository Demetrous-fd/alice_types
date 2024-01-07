from typing import List, Optional, Union
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4, field_serializer, field_validator

from alice_types import Button, Analytics
from alice_types.cards import BigImage, ImageGallery, ItemsList
from alice_types.validators import validate_tts_size, validate_dict_size
from alice_types.directives import AudioPlayerPlay, AudioPlayerStop, StartAccountLinking


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



class TextToSpeechModel(BaseModel):
    text: str = Field(
        default=...,
        max_length=1024,
        description="Текст, который следует показать и озвучить пользователю. Может быть пустым, если заполнено свойство tts."
    )
    tts: Optional[str] = Field(
        default=None,
        description="""
Ответ в формате TTS (text-to-speech). Максимум 1024 символа.
Теги <speaker>, которые используются для ссылок на звуки, не учитываются в ограничении в 1024 символа на длину значения свойства tts.
"""
    )

    validate_tts_size = field_validator("tts", mode="before")(
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


class Response(TextToSpeechModel):
    card: Optional[Union[BigImage, ItemsList, ImageGallery]] = Field(default=None)
    buttons: Optional[List[Button]] = Field(default_factory=list)
    end_session: bool = Field(default=False)
    directives: Optional[Union[AudioPlayerPlay, AudioPlayerStop, StartAccountLinking]] = Field(default=None)


class AliceResponse(BaseModel):
    response: Union[ShowResponse, Response] = Field(
        default=...,
        description="Данные для ответа пользователю."
    )
    session_state: Optional[dict] = Field(
        default=None,
        description="""
Объект, содержащий состояние навыка для хранения в контексте сессии.
Состояние сессии перестанет храниться, если в ответе навыка не вернуть свойство session_state. 
Если для запроса состояние не меняется, но его нужно хранить, навыку следует вернуть тот же объект session_state, что пришел в запросе.
"""
    )
    user_state_update: Optional[dict] = Field(
        default=None,
        description="""
Объект, содержащий состояние навыка для хранения в контексте авторизованного пользователя.
Чтобы удалить поле, записанное в состояние пользователя, навык должен отправить это поле со значением None (null).
"""
    )
    application_state: Optional[dict] = Field(
        default=None,
        description="""
Объект, содержащий состояние навыка для хранения в контексте экземпляра приложения пользователя.
Чтобы очистить сохраненное состояние приложения, навык может отправить это поле со значением {} — пустым словарем.
"""
    )
    analytics: Optional[Analytics] = Field(
        default=None,
        description="Объект с данными для аналитики. Доступен навыкам с подключенным параметром Настройки AppMetrica. "
    )
    version: str = Field(
        default=...,
        description="Версия протокола."
    )

    validate_session_state_size = field_validator("session_state", mode="before")(
        validate_dict_size(max_size=1024)
    )

    validate_user_state_size = field_validator("user_state_update", mode="before")(
        validate_dict_size(max_size=1024)
    )

    # TODO: Узнать максимальный размер application_state
    validate_application_state_size = field_validator("application_state", mode="before")(
        validate_dict_size(max_size=1024)
    )
