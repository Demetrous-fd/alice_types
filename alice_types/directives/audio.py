from decimal import Decimal
from typing import Literal
from enum import Enum

from pydantic import BaseModel, Field


class AudioActionType(str, Enum):
    PLAY = "Play"
    STOP = "Stop"


class AudioPlayerImage(BaseModel):
    url: str = Field(..., description="URL изображения")


class AudioPlayerStream(BaseModel):
    url: str = Field(..., description="URL аудиопотока.")
    offset_ms: Decimal = Field(..., description="Временная метка, с которой необходимо проигрывать трек.")
    token: str = Field(
        ...,
        description="Идентификатор потока. Может быть использован для кеширования изображений "
                    "или для постановки трека в очередь на стороне навыка."
    )


class AudioPlayerMetaData(BaseModel):
    title: str = Field(..., description="Описание трека. Например, название композиции.")
    sub_title: str = Field(..., description="Дополнительное описание трека. Например, имя артиста.")
    art: AudioPlayerImage = Field(..., description="Обложка альбома трека.")
    background_image: AudioPlayerImage = Field(..., description="Фоновое изображение.")


class AudioPlayerItem(BaseModel):
    stream: AudioPlayerStream = Field(..., description="Описание аудиопотока.")
    metadata: AudioPlayerMetaData = Field(..., description="Метаданные проигрываемого трека.")


class AudioPlayerPlay(BaseModel):
    action: Literal[AudioActionType.PLAY] = Field(..., description="Команда директивы.")
    item: AudioPlayerItem = Field(..., description="Описание трека и аудиопотока.")


class AudioPlayerStop(BaseModel):
    action: Literal[AudioActionType.STOP] = Field(..., description="Команда директивы.")
