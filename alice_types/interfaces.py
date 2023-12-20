from typing import Optional, List, Literal, Union
from enum import Enum

from pydantic import BaseModel, Field

INTERFACE_NAME = Literal["screen", "account_linking", "audio_player", "payments"]


class InterfaceType(str, Enum):
    SCREEN = "screen"
    AUDIO_PLAYER = "audio_player"
    ACCOUNT_LINKING = "account_linking"
    PAYMENTS = "payments"


class Interfaces(BaseModel):
    screen: Optional[dict] = Field(default=None)
    account_linking: Optional[dict] = Field(default=None)
    audio_player: Optional[dict] = Field(default=None)
    payments: Optional[dict] = Field(default=None)

    def available(self) -> List[INTERFACE_NAME]:
        available = []
        for name, value in self.__dict__.items():
            if value is not None:
                available.append(name)
        
        return available
    
    def has(self, interface: Union[InterfaceType, INTERFACE_NAME]) -> bool:
        if isinstance(interface, str) and interface not in InterfaceType._value2member_map_:
            raise ValueError(f"Interface: {interface} not exists")
        
        return self.__dict__.get(interface, None) is not None
