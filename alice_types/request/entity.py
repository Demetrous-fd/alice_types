from typing import Union, Optional, Literal, List

from pydantic import BaseModel, Field, RootModel

from alice_types.mixin import AvailableMixin
from alice_types.request.slots import SlotsType


class EntityValueFio(BaseModel, AvailableMixin):
    """
    Доступные методы:
    - available(self) -> Возвращает список доступных атрибутов объекта, у которых значение не равно None.
    """
    first_name: Optional[str] = Field(default=None)
    patronymic_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class EntityValueGeo(BaseModel, AvailableMixin):
    """
    Доступные методы:
    - available(self) -> Возвращает список доступных атрибутов объекта, у которых значение не равно None.
    """
    country: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    street: Optional[str] = Field(default=None)
    house_number: Optional[str] = Field(default=None)
    airport: Optional[str] = Field(default=None)


class EntityValueDatetime(BaseModel, AvailableMixin):
    """
    Доступные методы:
    - available(self) -> Возвращает список доступных атрибутов объекта, у которых значение не равно None.
    """
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


class EntityBase(BaseModel):
    """
    Модель, представляющая сущность.

    Доступные методы:
    - value.available(self) -> Возвращает список доступных атрибутов объекта, у которых значение не равно None. (Отсутствует у EntityString и EntityNumber)
    """
    type: str = Field(...)
    tokens: EntityTokens = Field(...)
    value: dict = Field(...)


class EntityNumber(EntityBase):
    type: Literal[SlotsType.YANDEX_NUMBER] = Field(...)
    value: Union[int, float] = Field(...)


class EntityGeo(EntityBase):
    type: Literal[SlotsType.YANDEX_GEO] = Field(...)
    value: EntityValueGeo = Field(...)


class EntityFio(EntityBase):
    type: Literal[SlotsType.YANDEX_FIO] = Field(...)
    value: EntityValueFio = Field(...)


class EntityDatetime(EntityBase):
    type: Literal[SlotsType.YANDEX_DATETIME] = Field(...)
    value: EntityValueDatetime = Field(...)


class EntityString(EntityBase):
    type: Literal[SlotsType.YANDEX_STRING] = Field(...)
    value: str = Field(...)


class Entities(RootModel):
    """
    Модель, представляющая группу сущностей.

    Доступные методы:
    - get(self, entity_type: Union[SlotsType, str]) -> Возвращает список сущностей заданного типа.
    """
    root: List[Union[
        EntityNumber,
        EntityString,
        EntityGeo,
        EntityDatetime,
        EntityFio,
        EntityBase
    ]]

    def get(self, entity_type: Union[SlotsType, str]) -> List[Union[
        EntityNumber,
        EntityString,
        EntityGeo,
        EntityDatetime,
        EntityFio,
        EntityBase
    ]]:
        """
        Возвращает список сущностей заданного типа.

        Args:
            entity_type (Union[SlotsType, str]): Тип сущности.

        Returns:
            Список сущностей заданного типа.
        """
        return [entity for entity in self.root if entity.type == entity_type]
