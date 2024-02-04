from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator

from alice_types.response import Analytics
from alice_types.mixin import ExcludeUnsetMixin
from alice_types.validators import validate_dict_size, DynamicSize
from alice_types.response.type import ShowResponse, Response


class AliceResponse(BaseModel, ExcludeUnsetMixin, validate_assignment=True):
    """
    Максимальный размер ответа составляет 131072 байт / 128 КибиБайт

    Пример 1:
    ```python
    reply = AliceResponse(
        response=Response(
            text="Привет 🖐"
        ),
        session_state={
            "current_state": "START"
        }
    )
    ```

    Пример 2:
    ```python
    reply = AliceResponse()
    reply.response.text = "Привет 🖐"
    reply.session_state = {
        "current_state": "START"
    }
    ```
    """
    response: Union[ShowResponse, Response] = Field(
        default_factory=Response,
        description="Данные для ответа пользователю."
    )
    session_state: Optional[dict] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="""
Объект, содержащий состояние навыка для хранения в контексте сессии.
Состояние сессии перестанет храниться, если в ответе навыка не вернуть свойство session_state. 
Если для запроса состояние не меняется, но его нужно хранить, навыку следует вернуть тот же объект session_state, что пришел в запросе.
Максимально достигнутый размер для SessionState: 130930 байт (PC; mini 2.)
"""
    )
    user_state_update: Optional[dict] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="""
Объект, содержащий состояние навыка для хранения в контексте авторизованного пользователя.
Чтобы удалить поле, записанное в состояние пользователя, навык должен отправить это поле со значением None (null).
Максимально достигнутый размер для UserState: 130930 байт * 10 (PC; mini 2.), но это не предел, возможно это из-за Беты Алисы.
"""
    )
    application_state: Optional[dict] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="""
Объект, содержащий состояние навыка для хранения в контексте экземпляра приложения пользователя.
Чтобы очистить сохраненное состояние приложения, навык может отправить это поле со значением {} — пустым словарем.
Максимально достигнутый размер для ApplicationState: 130930 байт (PC; mini 2.)
"""
    )
    analytics: Optional[Analytics] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Объект с данными для аналитики. Доступен навыкам с подключенным параметром Настройки AppMetrica. "
    )
    version: str = Field(
        default="1.0",
        description="Версия протокола."
    )

    validate_session_state_size = field_validator("session_state", mode="before")(
        validate_dict_size(max_size=DynamicSize("session_state", 1024))
    )

    validate_user_state_size = field_validator("user_state_update", mode="before")(
        validate_dict_size(max_size=DynamicSize("user_state_update", 1024))
    )

    validate_application_state_size = field_validator("application_state", mode="before")(
        validate_dict_size(max_size=DynamicSize("application_state", 1024))
    )

    @classmethod
    def set_session_state_limit_size(cls, max_size: int = 1024):
        DynamicSize("session_state", max_size)

    @classmethod
    def set_user_state_limit_size(cls, max_size: int = 1024):
        DynamicSize("user_state_update", max_size)

    @classmethod
    def set_application_state_limit_size(cls, max_size: int = 1024):
        DynamicSize("application_state", max_size)
