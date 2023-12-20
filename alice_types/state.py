from pydantic import BaseModel, Field


class State(BaseModel):
    session: dict = Field(default_factory=dict)
    user: dict = Field(default_factory=dict)
    application: dict = Field(default_factory=dict)
