from typing import Union, Optional, Literal

from pydantic import BaseModel, Field

from alice_types.common import AvailableMixin
from alice_types import SlotsType


class EntityValueFio(BaseModel, AvailableMixin):
    first_name: Optional[str] = Field(default=None)
    patronymic_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class EntityValueNumber(BaseModel, AvailableMixin):
    value: Optional[Union[int, float]] = Field(default=None)


class EntityValueGeo(BaseModel, AvailableMixin):
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    house_number: Optional[str] = Field(default=None)
    airport: Optional[str] = Field(default=None)


class EntityValueDatetime(BaseModel, AvailableMixin):
    year: Optional[int] = Field(default=None)
    year_is_relative: Optional[bool] = Field(default=None)
    
    month: Optional[int] = Field(default=None)
    month_is_relative: Optional[bool] = Field(default=None)
    
    day: Optional[int] = Field(default=None)
    day_is_relative: Optional[bool] = Field(default=None)
    
    hour: Optional[int] = Field(default=None)
    hour_is_relative: Optional[bool] = Field(default=None)
    
    minute: Optional[int] = Field(default=None)
    minute_is_relative: Optional[bool] = Field(default=None)


class EntityTokens(BaseModel):
    start: int = Field(...)
    end: int = Field(...)


# TODO: Add support for custom type
class EntityBase(BaseModel):
    type: str = Field(...)
    tokens: EntityTokens = Field(...)
    value: dict = Field(...)


class EntityNumber(EntityBase):
    type: Literal[SlotsType.YANDEX_NUMBER] = Field(...)
    value: EntityValueNumber = Field(...)


class EntityGeo(EntityBase):
    type: Literal[SlotsType.YANDEX_GEO] = Field(...)
    value: EntityValueGeo = Field(...)


class EntityFio(EntityBase):
    type: Literal[SlotsType.YANDEX_FIO] = Field(...)
    value: EntityValueFio = Field(...)


class EntityDatetime(EntityBase):
    type: Literal[SlotsType.YANDEX_DATETIME] = Field(...)
    value: EntityValueDatetime = Field(...)


# # TODO: Проверить реализован ли этот слот
# class EntityString(EntityBase):
#     type: Literal[SlotsType.YANDEX_STRING] = Field(...)
#     value: dict = Field(...)
