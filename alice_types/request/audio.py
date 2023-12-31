from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class RequestAudioType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-audioplayer.html
    AUDIO_PLAYER_PLAYBACK_STARTED = "AudioPlayer.PlaybackStarted"
    AUDIO_PLAYER_PLAYBACK_FINISHED = "AudioPlayer.PlaybackFinished"
    AUDIO_PLAYER_PLAYBACK_NEARLY_FINISHED = "AudioPlayer.PlaybackNearlyFinished"
    AUDIO_PLAYER_PLAYBACK_STOPPED = "AudioPlayer.PlaybackStopped"
    AUDIO_PLAYER_PLAYBACK_FAILED = "AudioPlayer.PlaybackFailed"


class RequestAudioErrorType(str, Enum):
    MEDIA_ERROR_UNKNOWN = "MEDIA_ERROR_UNKNOWN"
    MEDIA_ERROR_SERVICE_UNAVAILABLE = "MEDIA_ERROR_SERVICE_UNAVAILABLE"


class RequestAudioError(BaseModel):
    type: RequestAudioErrorType = Field(...)
    message: str = Field(...)


class RequestAudio(BaseModel):
    type: RequestAudioType = Field(...)
    error: Optional[RequestAudioError] = Field(default=None)

    def is_error(self) -> bool:
        return bool(self.error)

    @model_validator(mode="before")
    @classmethod
    def validate_error(cls, data: dict) -> dict:
        audio_type = data["type"]
        audio_type = RequestAudioType(audio_type)
        error = data.get("error", False)

        if error and audio_type != RequestAudioType.AUDIO_PLAYER_PLAYBACK_FAILED:
            raise ValueError(f"{audio_type} не относиться к событию ошибки воспроизведения.")
        elif error is False and audio_type == RequestAudioType.AUDIO_PLAYER_PLAYBACK_FAILED:
            raise ValueError("Событие ошибки воспроизведения должно иметь поле error.")

        return data
