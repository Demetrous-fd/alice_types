import pytest

from alice_types.response import AliceResponse
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
        alice = AliceResponse.model_validate_json(value.string)
        assert alice.model_dump_json().encode() == expected


def test_alice_response_size_validator():
    with pytest.raises(ValueError):
        AliceResponse.model_validate({
            "session_state": {
                "1": "1" * 2040
            },
            "user_state_update": {
                "1": "1" * 2040
            },
            "application_state": {
                "1": "1" * 2040
            },
        })

    AliceResponse.set_session_state_limit_size(2048)
    AliceResponse.set_user_state_limit_size(2048)
    AliceResponse.set_application_state_limit_size(2048)
    AliceResponse.model_validate({
        "session_state": {
            "1": "1" * 2040
        },
        "user_state_update": {
            "1": "1" * 2040
        },
        "application_state": {
            "1": "1" * 2040
        },
    })

    AliceResponse.set_session_state_limit_size(1024)
    AliceResponse.set_user_state_limit_size(1024)
    AliceResponse.set_application_state_limit_size(1024)
