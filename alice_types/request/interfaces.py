from typing import Optional, Literal, Union
from enum import Enum

from pydantic import BaseModel, Field

from alice_types.mixin import AvailableMixin

INTERFACE_NAME = Literal["screen", "account_linking", "audio_player", "payments"]


class InterfaceType(str, Enum):
    SCREEN = "screen"
    AUDIO_PLAYER = "audio_player"
    ACCOUNT_LINKING = "account_linking"
    PAYMENTS = "payments"


class Interfaces(BaseModel, AvailableMixin):
    screen: Optional[dict] = Field(default=None)
    account_linking: Optional[dict] = Field(default=None)
    audio_player: Optional[dict] = Field(default=None)
    payments: Optional[dict] = Field(default=None)
    
    def has(self, interface: Union[InterfaceType, INTERFACE_NAME]) -> bool:
        """
        Проверяет, существует ли этот интерфейс.
        """
        if isinstance(interface, str) and interface not in InterfaceType._value2member_map_:
            raise ValueError(f"Interface: {interface} not exists")
        
        return self.__dict__.get(interface, None) is not None
