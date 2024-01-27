from typing import List, Union

from pydantic import BaseModel, Field

from alice_types.request.intents import Intent, IntentType
from alice_types.request import entity


class NaturalLanguageUnderstanding(BaseModel):
    tokens: List[str] = Field(default_factory=list)
    entities: List[Union[
        entity.EntityNumber,
        entity.EntityString,
        entity.EntityGeo, 
        entity.EntityDatetime,
        entity.EntityFio,
        entity.EntityBase,
        dict
    ]] = Field(default_factory=list) # TODO: DynamicFieldsTypeMixin + tests
    intents: dict[Union[IntentType, str], Intent] = Field(default_factory=dict) # TODO: DynamicFieldsTypeMixin + tests
