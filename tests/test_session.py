import pytest

from alice_types.request.session import Session, User, Application
import dataset


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.SESSION_USER["NOT_EMPTY"]],
        *[data.values() for data in dataset.SESSION_USER["ERROR"]],
    ]
)
def test_session_user(obj, expected, raise_handler):
    with raise_handler:
        user = User.model_validate_json(obj.string)
        assert user.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.SESSION_APPLICATION["NOT_EMPTY"]],
        *[data.values() for data in dataset.SESSION_APPLICATION["ERROR"]],
    ]
)
def test_session_application(obj, expected, raise_handler):
    with raise_handler:
        application = Application.model_validate_json(obj.string)
        assert application.model_dump_json(exclude_none=True).encode() == expected


@pytest.mark.parametrize(
    ["obj", "expected", "raise_handler"],
    [
        *[data.values() for data in dataset.SESSION["NOT_EMPTY"]],
        *[data.values() for data in dataset.SESSION["ERROR"]],
    ]
)
def test_session(obj, expected, raise_handler):
    with raise_handler:
        session = Session.model_validate_json(obj.string)
        assert session.model_dump_json(exclude_none=True).encode() == expected
