from enum import Enum

from pydantic import BaseModel, Field
from alice_types import request


class GameState(str, Enum):
    ANY = "*"
    START = "START"
    TURN = "TURN"


class SessionState(BaseModel):
    current_state: GameState = Field(default=GameState.ANY)
    previous_state: GameState = Field(default=GameState.ANY)


request.State.extend_session_model(SessionState)
# request.State.extend_user_model(UserState)
# request.State.extend_application_model(ApplicationState)

data = {
    "session": {"current_state": "START"}
}
state = request.State.model_validate(data)

assert isinstance(state.session, SessionState)
assert all([
    state.session.current_state == GameState.START,
    state.session.previous_state == "*"
])

state.session.previous_state = state.session.current_state
state.session.current_state = GameState.TURN

data = state.model_dump()

assert all([
    data["session"]["current_state"] == GameState.TURN,
    data["session"]["previous_state"] == GameState.START
])
