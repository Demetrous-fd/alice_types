from typing import List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field
    

class AudioActionType(str, Enum):
    START = "Start"
    STOP = "Stop"


class AudioPlayer(BaseModel):
    action: AudioActionType = Field(...)


class StartAccountLinking(BaseModel):
    pass


