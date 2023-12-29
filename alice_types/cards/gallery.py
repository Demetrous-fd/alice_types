from typing import Literal

from pydantic import BaseModel, Field, conlist, model_validator

from alice_types.cards.base import CardType, Item


class ImageGallery(BaseModel):
    type: Literal[CardType.IMAGE_GALLERY] = Field(default=CardType.IMAGE_GALLERY, frozen=True)
    items: conlist(Item, min_length=1, max_length=10) = Field(...)  # type: ignore

    @model_validator(mode='after')
    def validate(self):
        for item in self.items:
            item.description = None
        return self
