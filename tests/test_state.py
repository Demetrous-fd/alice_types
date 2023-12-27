from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field
import pytest
import orjson

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
        
        
def test_state_with_custom_fields_type():
    class GameState(str, Enum):
        START = "START"
        ANY = "*"
        
    class SessionState(BaseModel):
        current_state: GameState = Field(default=GameState.ANY)
        previous_state: GameState = Field(default=GameState.ANY)
        
    class UserState(BaseModel):
        username: Optional[str] = Field(default=None)
        
    State.set_session_model(SessionState)
    State.set_user_model(UserState)
    
    data = orjson.dumps({
        "session": {"current_state": "START"},
        "user": {},
        "application": {"storage": {"last_login": "01.01.1900"}}
    })
    
    state = State.model_validate_json(data)
    assert isinstance(state.session, SessionState)
    assert isinstance(state.user, UserState)
    assert isinstance(state.application, dict)
    
    
    assert all([
        state.session.current_state == GameState.START,
        state.session.previous_state == "*",
        state.user.username == None,
        state.application["storage"]["last_login"] == "01.01.1900"
    ])
    
    state.user.username = "Someone"
    state.application["storage"]["last_login"] = "31.12.2023"
    check_data = orjson.dumps({
        "session": {"current_state": "START", "previous_state": "*"},
        "user": {"username": state.user.username},
        "application": {"storage": {"last_login": "31.12.2023"}}
    })
    assert state.model_dump_json(exclude_none=True).encode() == check_data
