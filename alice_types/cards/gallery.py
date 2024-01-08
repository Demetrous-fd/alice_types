from typing import Literal

from pydantic import BaseModel, Field, conlist, model_validator

from alice_types.cards.base import CardType, CardItem


class ImageGallery(BaseModel):
    type: Literal[CardType.IMAGE_GALLERY] = Field(default=CardType.IMAGE_GALLERY, frozen=True)
    items: conlist(CardItem, min_length=1, max_length=10) = Field(...)
