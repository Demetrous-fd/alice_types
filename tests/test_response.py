import pytest

import alice_types
import dataset


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.ALICE_RESPONSE["NOT_EMPTY"]],
        *[data.values() for data in dataset.ALICE_RESPONSE["ERROR"]],
    ]
)
def test_alice_response(value, expected, raise_handler):
    with raise_handler:
        alice = alice_types.AliceResponse.model_validate_json(value.string)
        assert alice.model_dump_json(exclude_none=True).encode() == expected