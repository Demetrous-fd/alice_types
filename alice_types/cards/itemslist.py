from typing import Optional, Literal

from pydantic import BaseModel, Field, conlist

from alice_types.cards.base import CardItem, CardType
from alice_types.mixin import ExcludeUnsetMixin
from alice_types import Button


class Header(BaseModel):
    text: str = Field(..., max_length=64)


class Footer(BaseModel, ExcludeUnsetMixin):
    text: str = Field(..., max_length=64)
    button: Optional[Button] = Field(default=None, json_schema_extra={"exclude_unset": True})


class ItemsList(BaseModel, ExcludeUnsetMixin):
    type: Literal[CardType.ITEMS_LIST] = Field(default=CardType.ITEMS_LIST, frozen=True)
    header: Optional[Header] = Field(default=None, json_schema_extra={"exclude_unset": True})
    items: conlist(CardItem, min_length=1, max_length=5) = Field(
        default=...
    )
    footer: Optional[Footer] = Field(default=None, json_schema_extra={"exclude_unset": True})
