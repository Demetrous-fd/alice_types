from typing import Literal, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field

from alice_types.mixin import ExcludeUnsetMixin


class AudioActionType(str, Enum):
    PLAY = "Play"
    STOP = "Stop"


class AudioPlayerImage(BaseModel):
    url: str = Field(..., description="URL изображения")


class AudioPlayerStream(BaseModel):
    url: str = Field(..., description="URL аудиопотока.")
    offset_ms: int = Field(..., description="Временная метка, с которой необходимо проигрывать трек.")
    token: str = Field(
        ...,
        description="Идентификатор потока. Может быть использован для кеширования изображений "
                    "или для постановки трека в очередь на стороне навыка."
    )


class AudioPlayerMetaData(BaseModel, ExcludeUnsetMixin):
    title: Optional[str] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Описание трека. Например, название композиции."
    )
    sub_title: Optional[str] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Дополнительное описание трека. Например, имя артиста."
    )
    art: Optional[AudioPlayerImage] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Обложка альбома трека."
    )
    background_image: Optional[AudioPlayerImage] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Фоновое изображение."
    )


class AudioPlayerItem(BaseModel, ExcludeUnsetMixin):
    stream: AudioPlayerStream = Field(..., description="Описание аудиопотока.")
    metadata: Optional[AudioPlayerMetaData] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True},
        description="Метаданные проигрываемого трека."
    )


class AudioPlayerPlay(BaseModel):
    action: Literal[AudioActionType.PLAY] = Field(..., description="Команда директивы.")
    item: AudioPlayerItem = Field(..., description="Описание трека и аудиопотока.")


class AudioPlayerStop(BaseModel):
    action: Literal[AudioActionType.STOP] = Field(..., description="Команда директивы.")


class AudioPlayer(BaseModel):
    audio_player: Union[AudioPlayerPlay, AudioPlayerStop] = Field(...)
