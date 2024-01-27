from typing import Optional, Union

from pydantic import BaseModel, Field

from alice_types.mixin import ExcludeUnsetMixin
from .account import StartAccountLinking
from .audio import AudioPlayerPlay, AudioPlayerStop


class Directives(BaseModel, ExcludeUnsetMixin):
    audio_player: Optional[Union[AudioPlayerPlay, AudioPlayerStop]] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True}
    )
    start_account_linking: Optional[StartAccountLinking] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True}
    )
