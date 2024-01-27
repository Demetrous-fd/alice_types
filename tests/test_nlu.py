import pytest

from alice_types.request import NaturalLanguageUnderstanding
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
        nlu = NaturalLanguageUnderstanding.model_validate_json(value.string)
        assert nlu.model_dump_json(exclude_none=True).encode() == expected
