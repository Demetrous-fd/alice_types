from decimal import Decimal
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class PurchasePayload(BaseModel):
    id: str = Field(...)
    status: str = Field(...)
    paid: bool = Field(...)
    amount: Decimal = Field(...)
    currency: Optional[str] = Field(default="RUB")


class GameState(str, Enum):
    START = "START"
    ANY = "*"


class SessionState(BaseModel):
    current_state: GameState = Field(default=GameState.ANY)
    previous_state: GameState = Field(default=GameState.ANY)


class UserState(BaseModel):
    username: Optional[str] = Field(default=None)
