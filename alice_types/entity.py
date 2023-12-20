from pydantic import BaseModel, Field

from alice_types import SlotsType


class EntityTokens(BaseModel):
    start: int = Field(...)
    end: int = Field(...)


class Entity(BaseModel):
    type: SlotsType | str = Field(...)
    tokens: EntityTokens = Field(...)
    value: dict = Field(...)
