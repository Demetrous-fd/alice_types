from typing import List

from pydantic import BaseModel, Field

from alice_types.request.intents import Intents
from alice_types.request.entity import Entities


class NaturalLanguageUnderstanding(BaseModel):
    tokens: List[str] = Field(default_factory=list)
    entities: Entities = Field(...)
    intents: Intents = Field(...)
