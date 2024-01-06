import pytest

from alice_types import request
import dataset
import schemes


@pytest.mark.parametrize(
    ["value", "expected", "is_ping", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_SIMPLE_UTTERANCE["NOT_EMPTY"]],
        *[data.values() for data in dataset.REQUEST_SIMPLE_UTTERANCE["ERROR"]],
    ]
)
def test_simple_utterance_request(value, expected, is_ping, raise_handler):
    with raise_handler:
        simple_request = request.RequestSimpleUtterance.model_validate_json(value.string)
        assert simple_request.is_ping() == is_ping
        assert simple_request.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_BUTTON_PRESSED["NOT_EMPTY"]],
        *[data.values() for data in dataset.REQUEST_BUTTON_PRESSED["ERROR"]],
    ]
)
def test_button_pressed_request(value, expected, raise_handler):
    with raise_handler:
        button_request = request.RequestButtonPressed.model_validate_json(value.string)
        assert button_request.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_SHOW["NOT_EMPTY"]],
        *[data.values() for data in dataset.REQUEST_SHOW["ERROR"]],
    ]
)
def test_show_request(value, expected, raise_handler):
    with raise_handler:
        show_request = request.RequestShow.model_validate_json(value.string)
        assert show_request.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "has_error", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_AUDIO["ERROR"]],
        *[data.values() for data in dataset.REQUEST_AUDIO["NOT_EMPTY"]]
    ]
)
def test_audio_request(value, expected, has_error, raise_handler):
    with raise_handler:
        audio_request = request.RequestAudio.model_validate_json(value.string)
        
        if has_error:
            assert isinstance(audio_request.error, request.audio.RequestAudioError) and audio_request.is_error()
        else:
            assert audio_request.error is None and audio_request.is_error() is False
            
        assert audio_request.model_dump_json(exclude_none=True, by_alias=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_PURCHASE["NOT_EMPTY"]],
        *[data.values() for data in dataset.REQUEST_PURCHASE["ERROR"]],
    ]
)
def test_purchase_request(value, expected, raise_handler):
    with raise_handler:
        purchase_request = request.RequestPurchase.model_validate_json(value.string)
        assert purchase_request.model_dump_json(exclude_none=True, by_alias=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.REQUEST_PURCHASE["CUSTOM"]],
    ]
)
def test_purchase_request_with_custom_field(value, expected, raise_handler, override_purchase_payload_request_field):    
    with raise_handler:
        purchase_request = request.RequestPurchase.model_validate_json(value.string)
        assert isinstance(purchase_request.payload, schemes.PurchasePayload), \
            f"{purchase_request.payload=}; {isinstance(purchase_request.payload, schemes.PurchasePayload)}"
        assert purchase_request.model_dump_json(exclude_none=True, by_alias=True).encode() == expected


@pytest.mark.parametrize(
    ["value", "expected", "check_type", "raise_handler"],
    [
        *[data.values() for data in dataset.ALICE_REQUEST["NOT_EMPTY"]],
        *[data.values() for data in dataset.ALICE_REQUEST["ERROR"]],
    ]
)
def test_alice_request(value, expected, check_type, raise_handler):
    with raise_handler:
        alice_request = request.AliceRequest.model_validate_json(value.string)

        for field_name, _type_ in check_type.items():
            field = alice_request.__dict__[field_name]
            assert isinstance(field, _type_)

        assert alice_request.model_dump_json(exclude_none=True, by_alias=True).encode() == expected
