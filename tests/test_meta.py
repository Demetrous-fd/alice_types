import pytest

from alice_types import Meta
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.META["NOT_EMPTY"]],
        *[data.values() for data in dataset.META["ERROR"]],
    ]
)
def test_meta(value, expected, raise_handler):
    with raise_handler:
        event = Meta.model_validate_json(value.string)
        assert event.model_dump_json(exclude_none=True).encode() == expected
