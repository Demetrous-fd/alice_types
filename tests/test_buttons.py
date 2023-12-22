import pytest

from alice_types import Button
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        dataset.BUTTON["NOT_EMPTY"][0].values(),
        dataset.BUTTON["NOT_EMPTY"][1].values(),
        dataset.BUTTON["NOT_EMPTY"][2].values(),
        dataset.BUTTON["ERROR"][0].values(),
        dataset.BUTTON["ERROR"][1].values(),
        dataset.BUTTON["ERROR"][2].values(),
        dataset.BUTTON["ERROR"][3].values(),
    ]
)
def test_buttons(value, expected, raise_handler):
    with raise_handler:
        event = Button.model_validate_json(value.string)
        assert event.model_dump_json(exclude_none=True).encode() == expected
