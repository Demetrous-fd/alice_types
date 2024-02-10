from typing import Union, Optional, Literal, List, Iterable
from datetime import datetime

from pydantic import BaseModel, Field, RootModel
from dateutil.relativedelta import relativedelta
import pytz

from alice_types.request.slots import SlotsType
from alice_types.mixin import AvailableMixin


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

    def to_datetime(
            self,
            timezone: Optional[Union[pytz.BaseTzInfo, str]] = None
    ) -> datetime:
        if isinstance(timezone, str):
            timezone = pytz.timezone(timezone)

        date = datetime.now(tz=timezone).replace(hour=0, minute=0, second=0, microsecond=0)

        data = {
            "years" if self.year_is_relative is True else "year": self.year,
            "months" if self.month_is_relative is True else "month": self.month,
            "days" if self.day_is_relative is True else "day": self.day,
            "hours" if self.hour_is_relative is True else "hour": self.hour,
            "minutes" if self.minute is True else "minute": self.minute,
        }
        timedelta = relativedelta(**data)
        date += timedelta
        return date


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

    def to_datetime(
            self,
            timezone: Optional[Union[pytz.BaseTzInfo, str]] = None
    ) -> datetime:
        return self.value.to_datetime(timezone=timezone)


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
        return [entity for entity in self if entity.type == entity_type]

    def __len__(self) -> int:
        return len(self.root)

    def __iter__(self) -> Iterable[Union[
        EntityNumber,
        EntityString,
        EntityGeo,
        EntityDatetime,
        EntityFio,
        EntityBase
    ]]:
        return iter(self.root)

    def __getitem__(self, item) -> Union[
        EntityNumber,
        EntityString,
        EntityGeo,
        EntityDatetime,
        EntityFio,
        EntityBase
    ]:
        return self.root[item]
