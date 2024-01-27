import pytest

from alice_types.response import Button
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.BUTTON["NOT_EMPTY"]],
        *[data.values() for data in dataset.BUTTON["ERROR"]],
    ]
)
def test_buttons(value, expected, raise_handler):
    with raise_handler:
        event = Button.model_validate_json(value.string)
        assert event.model_dump_json(exclude_none=True).encode() == expected
