from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class Intent(BaseModel):
    slots: Optional[dict] = Field(default=None)


class IntentType(str, Enum):
    YANDEX_CONFIRM = "YANDEX.CONFIRM"
    YANDEX_REJECT = "YANDEX.REJECT"
    YANDEX_HELP = "YANDEX.HELP"
    YANDEX_REPEAT = "YANDEX.REPEAT"
    YANDEX_WHAT_CAN_YOU_DO = "YANDEX.WHAT_CAN_YOU_DO"
    YANDEX_BOOK_NAVIGATION_NEXT = "YANDEX.BOOK.NAVIGATION.NEXT"
    