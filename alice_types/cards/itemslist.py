from typing import Optional, Literal

from pydantic import BaseModel, Field, field_validator, conlist

from alice_types.cards.base import Item, CardType
from alice_types import Button


class Header(BaseModel):
    text: str = Field(..., max_length=64)


class Footer(BaseModel):
    text: str = Field(..., max_length=64)
    button: Optional[Button] = Field(default=None)

    @field_validator("button", mode="after")
    @classmethod
    def validate_button(cls, button: Button) -> Button:
        if button.hide:
            button.hide = False
        return button


class ItemsList(BaseModel):
    type: Literal[CardType.ITEMS_LIST] = Field(default=CardType.ITEMS_LIST, frozen=True)
    header: Optional[Header] = Field(default=None)
    items: conlist(Item, min_length=1, max_length=5) = Field(...) # type: ignore
    footer: Optional[Footer] = Field(default=None)
