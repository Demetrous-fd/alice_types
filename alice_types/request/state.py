from typing import Type, Union

from pydantic import BaseModel, Field, ConfigDict, SerializeAsAny

from alice_types.mixin import DynamicFieldsTypeMixin


class State(BaseModel, DynamicFieldsTypeMixin):
    model_config = ConfigDict(extra="allow")
    session: SerializeAsAny[Union[dict, BaseModel]] = Field(default_factory=dict)
    user: SerializeAsAny[Union[dict, BaseModel]] = Field(default_factory=dict)
    application: SerializeAsAny[Union[dict, BaseModel]] = Field(default_factory=dict)

    @classmethod
    def extend_session_model(cls, model: Type[BaseModel]) -> None:
        cls.extend_field_type("session", model)

    @classmethod
    def extend_user_model(cls, model: Type[BaseModel]) -> None:
        cls.extend_field_type("user", model)

    @classmethod
    def extend_application_model(cls, model: Type[BaseModel]) -> None:
        cls.extend_field_type("application", model)
