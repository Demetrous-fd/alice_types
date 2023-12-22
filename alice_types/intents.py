from typing import Any, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field


# TODO: Add other Build-In intents
class IntentType(str, Enum):
    # Default
    YANDEX_CONFIRM = "YANDEX.CONFIRM"
    YANDEX_REJECT = "YANDEX.REJECT"
    YANDEX_HELP = "YANDEX.HELP"
    YANDEX_REPEAT = "YANDEX.REPEAT"
    YANDEX_WHAT_CAN_YOU_DO = "YANDEX.WHAT_CAN_YOU_DO"
    
    # Book
    YANDEX_BOOK_NAVIGATION_NEXT = "YANDEX.BOOK.NAVIGATION.NEXT"
    


class Intent(BaseModel):
    slots: Optional[dict[str, Any]] = Field(default=None)
