import pytest

from alice_types import Interfaces, InterfaceType


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
                '{"screen": {},"payments": {},"account_linking": {}}',
                [InterfaceType.SCREEN, InterfaceType.ACCOUNT_LINKING, InterfaceType.PAYMENTS]
        )
    ]
)
def test_interface(test_input, expected):
    interfaces = Interfaces.model_validate_json(test_input)

    assert interfaces.available() == expected

    for interface in expected:
        assert interfaces.has(interface), f"{interfaces=} not contain {interface}"

    assert interfaces.has(InterfaceType.AUDIO_PLAYER) is False

    with pytest.raises(ValueError):
        interfaces.has("nothing")
        interfaces.has(None)
