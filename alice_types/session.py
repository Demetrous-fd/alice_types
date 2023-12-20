from typing import Optional, Any
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from .logger import logger

USER_ID_DEPRECATED_MESSAGE = "Свойство не поддерживается — вместо него следует использовать новое, " \
                             "полностью аналогичное свойство session.application.application_id"


class User(BaseModel):
    user_id: str = Field(...)
    access_token: Optional[str] = Field(default=None)


class Application(BaseModel):
    application_id: str = Field(..., max_length=64)


class BaseSession(BaseModel):
    message_id: Decimal = Field(..., max_digits=8)
    session_id: str = Field(..., max_length=64)
    user_id: Optional[str] = Field(
        default=None,
        description=USER_ID_DEPRECATED_MESSAGE
    )
    
    @model_validator(mode="before") # type: ignore
    @classmethod
    def validate_fields(cls, data: Any):
        if isinstance(data, dict):
            if data.get("user_id", None):
                logger.info(USER_ID_DEPRECATED_MESSAGE)
                
        return data
    

class Session(BaseSession):
    "https://yandex.ru/dev/dialogs/alice/doc/request.html#request__session-desc"
    new: bool = Field(default=False)
    skill_id: str = Field(...)
    user: Optional[User] = Field(
        default=None, 
        description="Атрибуты пользователя Яндекса, который взаимодействует с навыком. " \
                    "Если пользователь не авторизован в приложении, свойства user в запросе не будет."
    )
    
    application: Application = Field(
        ..., 
        description="Данные о приложении, с помощью которого пользователь взаимодействует с навыком."
    )
