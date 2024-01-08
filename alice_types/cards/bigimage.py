from typing import Literal, Optional

from pydantic import Field

from alice_types.cards.base import CardItem, CardType


class BigImage(CardItem):
    type: Literal[CardType.BIG_IMAGE] = Field(default=CardType.BIG_IMAGE, frozen=True)
    description: Optional[str] = Field(default=None, max_length=1024, exclude_unset=True)
