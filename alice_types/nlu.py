from typing import List, Union

from pydantic import BaseModel, Field

from alice_types import Intent, IntentType
from alice_types import entity


class NaturalLanguageUnderstanding(BaseModel):
    tokens: List[str] = Field(default_factory=list)
    entities: List[Union[
        entity.EntityNumber, 
        entity.EntityGeo, 
        entity.EntityDatetime,
        entity.EntityFio,
        entity.EntityBase
    ]] = Field(default_factory=list)
    intents: dict[Union[IntentType, str], Intent] = Field(default_factory=dict)
