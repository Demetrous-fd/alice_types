from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


USER_ID_DEPRECATED_MESSAGE = "Свойство не поддерживается — вместо него следует использовать новое, " \
                             "полностью аналогичное свойство session.application.application_id"


class User(BaseModel):
    user_id: str = Field(...)
    access_token: Optional[str] = Field(default=None)


class Application(BaseModel):
    application_id: str = Field(..., max_length=64)


class BaseSession(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            Decimal: int
        }
    )

    message_id: Decimal = Field(..., max_digits=8)
    session_id: str = Field(..., max_length=64)
    user_id: Optional[str] = Field(
        default=None,
        description=USER_ID_DEPRECATED_MESSAGE
    )
    

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
