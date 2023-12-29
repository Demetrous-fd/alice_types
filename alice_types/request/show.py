from enum import Enum

from pydantic import BaseModel, Field


class RequestShowType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-show-pull.html
    SHOW_PULL = "Show.Pull"


class ShowType(str, Enum):
    MORNING = "MORNING"


class RequestShow(BaseModel):
    type: RequestShowType = Field(...)
    show_type: ShowType = Field(...)
