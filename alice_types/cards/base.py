from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, model_validator

from alice_types import Button  # type: ignore


class CardType(str, Enum):
    BIG_IMAGE = "BigImage"
    IMAGE_GALLERY = "ImageGallery"
    ITEMS_LIST = "ItemsList"


class Item(BaseModel):
    image_id: str = Field(...)
    title: str = Field(..., max_length=128)
    button: Optional[Button] = Field(default=None, description="Свойства кликабельного изображения.")
    description: Optional[str] = Field(default=None, max_length=256)

    @model_validator(mode='after')
    def validate(self):
        if self.button:
            self.button.hide = False
        return self
