from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class RequestAudioType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    AUDIO_PLAYER_PLAYBACK_STARTED = "AudioPlayer.PlaybackStarted"
    AUDIO_PLAYER_PLAYBACK_FINISHED = "AudioPlayer.PlaybackFinished"
    AUDIO_PLAYER_PLAYBACK_NEARLY_FINISHED =  "AudioPlayer.PlaybackNearlyFinished"
    AUDIO_PLAYER_PLAYBACK_STOPPED = "AudioPlayer.PlaybackStopped"
    AUDIO_PLAYER_PLAYBACK_FAILED = "AudioPlayer.PlaybackStopped"


class RequestAudioErrorType(str, Enum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"


class RequestAudioError(BaseModel):
    message: str = Field(...)
    type: RequestAudioErrorType = Field(...)


class RequestAudio(BaseModel):
    type: RequestAudioType
    error: Optional[RequestAudioError] = Field(default=None)

    def has_error(self) -> bool:
        return bool(self.error)
