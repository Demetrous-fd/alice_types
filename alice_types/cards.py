from typing import Optional, Literal
from enum import Enum

from pydantic import BaseModel, Field, field_validator, conlist, model_validator

from alice_types import Button # type: ignore


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


class BigImage(Item):
    type: Literal[CardType.BIG_IMAGE] = Field(default=CardType.BIG_IMAGE, frozen=True)
    description: str = Field(..., max_length=1024)
    

class ImageGallery(BaseModel):
    type: Literal[CardType.IMAGE_GALLERY] = Field(default=CardType.IMAGE_GALLERY, frozen=True)
    items: conlist(Item, min_length=1, max_length=10) # type: ignore

    @model_validator(mode='after')
    def validate(self):
        for item in self.items:
            item.description = None
        return self
    

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
    items: conlist(Item, min_length=1, max_length=5) # type: ignore
    footer: Optional[Footer] = Field(default=None)
