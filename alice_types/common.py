from typing import Type, ClassVar, List, Any, Union
from collections import defaultdict

from pydantic import BaseModel, model_validator, ValidationError


class AvailableMixin:
    def available(self) -> List[str]:
        available = []
        for name, value in self.__dict__.items():
            if value is not None:
                available.append(name)
        
        return available


class DynamicFieldsType(BaseModel):
    __extended_fields_type__: ClassVar[dict[str, List[Type[BaseModel]]]] = defaultdict(list)
    
    @classmethod
    def extend_field_type(cls, field_name: str, new_type: Type[BaseModel]) -> None:
        if issubclass(new_type, BaseModel) is False:
            raise ValueError("The type must be inherited from pydantic.BaseModel")
        cls.__extended_fields_type__[field_name].append(new_type)
        
        field_annotation = cls.__annotations__[field_name]
        cls.__annotations__[field_name] = Union[new_type, *field_annotation.__args__]
        
    @model_validator(mode="before")
    @classmethod
    def validate_model(cls, data: Any) -> Any:
        for field, types in cls.__extended_fields_type__.items():
            value = data.get(field, {})
            for _type_ in types:
                if any([isinstance(value, dict), isinstance(value, bytes), isinstance(value, str)]) is False:
                    continue
                
                try:
                    value = _type_(**value) if isinstance(value, dict) else _type_.model_validate_json(value) # type: ignore
                    data[field] = value
                except ValidationError:
                    continue
                
        return data
