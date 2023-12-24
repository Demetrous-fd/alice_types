import pytest

from alice_types import Intent
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.INTENTS["EMPTY"]],
        *[data.values() for data in dataset.INTENTS["NOT_EMPTY"]],
    ]
)
def test_intents(value, expected, raise_handler):
    with raise_handler:
        intents = Intent.model_validate_json(value.string)
        assert intents.model_dump_json(exclude_none=True).encode() == expected
