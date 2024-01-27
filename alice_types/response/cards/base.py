from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field

from alice_types.response import Button
from alice_types.mixin import ExcludeUnsetMixin


class CardType(str, Enum):
    BIG_IMAGE = "BigImage"
    IMAGE_GALLERY = "ImageGallery"
    ITEMS_LIST = "ItemsList"


class CardItem(BaseModel, ExcludeUnsetMixin):
    image_id: str = Field(...)
    title: Optional[str] = Field(default=None, max_length=128, json_schema_extra={"exclude_unset": True})
    button: Optional[Button] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Свойства кликабельного изображения.",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=256,
        json_schema_extra={"exclude_unset": True},
        description="Описание карточки, можно использовать на любом типе карточек."
    )
