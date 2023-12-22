import pytest

from alice_types import NaturalLanguageUnderstanding
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.NLU["EMPTY"]],
        *[data.values() for data in dataset.NLU["NOT_EMPTY"]],
        *[data.values() for data in dataset.NLU["ERROR"]],
    ]
)
def test_nlu(value, expected, raise_handler):
    with raise_handler:
        event = NaturalLanguageUnderstanding.model_validate_json(value.string)
        assert event.model_dump_json(exclude_none=True).encode() == expected
