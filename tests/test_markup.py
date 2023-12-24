import pytest

from alice_types import Markup
import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.MARKUP["EMPTY"]],
        *[data.values() for data in dataset.MARKUP["NOT_EMPTY"]],
        *[data.values() for data in dataset.MARKUP["ERROR"]],
    ]
)
def test_markup(obj, expected, raise_handler):
    with raise_handler:
        markup = Markup.model_validate_json(obj.string)
        assert markup.model_dump_json().encode() == expected
    
