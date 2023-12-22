import pytest

from alice_types import Markup
import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        dataset.MARKUP["ERROR"][0].values(),
        dataset.MARKUP["EMPTY"][0].values(),
        dataset.MARKUP["EMPTY"][1].values(),
        dataset.MARKUP["NOT_EMPTY"][0].values(),
    ]
)
def test_markup(obj, expected, raise_handler):
    with raise_handler:
        markup = Markup.model_validate_json(obj.string)
        assert markup.model_dump_json().encode() == expected
    
