import pytest

from alice_types.directives import audio
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "command", "raise_handler"],
    [
        *[data.values() for data in dataset.AUDIO_PLAYER_DIRECTIVE["NOT_EMPTY"]],
        *[data.values() for data in dataset.AUDIO_PLAYER_DIRECTIVE["ERROR"]]
    ]
)
def test_audio_player(value, expected, command, raise_handler):
    with raise_handler:
        player = audio.AudioPlayer.model_validate_json(value.string)
        assert isinstance(player.audio_player, command)
        assert player.model_dump_json(exclude_none=True).encode() == expected
