import pytest

from alice_types import State
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.STATE["EMPTY"]],
        *[data.values() for data in dataset.STATE["NOT_EMPTY"]],
        *[data.values() for data in dataset.STATE["ERROR"]],
    ]
)
def test_state(value, expected, raise_handler):
    with raise_handler:
        state = State.model_validate_json(value.string)
        assert state.model_dump_json(exclude_none=True).encode() == expected
