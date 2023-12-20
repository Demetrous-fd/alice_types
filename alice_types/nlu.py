from typing import List

from pydantic import BaseModel, Field

from alice_types import Entity, Intent


class NaturalLanguageUnderstanding(BaseModel):
    tokens: List[str] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    intents: dict[str, Intent] = Field(default_factory=dict)
