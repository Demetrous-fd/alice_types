from typing import List, Union

from pydantic import BaseModel, Field

from alice_types.request.intents import Intent, IntentType
from alice_types.request.entity import Entities


class NaturalLanguageUnderstanding(BaseModel):
    tokens: List[str] = Field(default_factory=list)
    entities: Entities = Field(...)
    intents: dict[Union[IntentType, str], Intent] = Field(default_factory=dict)
