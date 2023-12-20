from typing import Literal

from pydantic import Field

from alice_types.cards.base import Item, CardType


class BigImage(Item):
    type: Literal[CardType.BIG_IMAGE] = Field(default=CardType.BIG_IMAGE, frozen=True)
    description: str = Field(..., max_length=1024)
