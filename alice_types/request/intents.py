from typing import Any, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field, RootModel


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


class Intents(RootModel):
    root: dict[Union[IntentType, str], Intent]

    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
