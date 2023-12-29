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
    

class DynamicFieldsTypeMixin:
    """
    Этот класс предназначен для обработки динамических типов полей путем их расширения во время выполнения.
    
    Расширяемые поля должны иметь тип: SerializeAsAny[Union[dict, BaseModel]]
    
    Example:
    
    from typing import Union
    
    from pydantic import BaseModel, SerializeAsAny
    
    from alice_types.mixin import DynamicFieldsTypeMixin
    
    
    class Example(BaseModel, DynamicFieldsTypeMixin):
        payload: SerializeAsAny[Union[dict, BaseModel]]
        
    
    class ExtendPayload(BaseModel):
        name: str
        
    
    Example.extend_field_type("payload", ExtendPayload)
    """
    __extended_fields_type__: ClassVar[dict[str, List[Type[BaseModel]]]] = defaultdict(list)
    
    @classmethod
    def extend_field_type(cls, field_name: str, new_type: Type[BaseModel]) -> None:
        """
        Args:
            field_name (str): Наименование поля
            new_type (Type[BaseModel]): Pydantic модель

        Raises:
            ValueError: Возникает, если new_type не является подклассом pydantic.BaseModel
        """
        if issubclass(new_type, BaseModel) is False:
            raise ValueError("The type must be inherited from pydantic.BaseModel")
        if new_type in cls.__extended_fields_type__:
            return
        
        fields_name = [field_name]
        if alias := cls.model_fields[field_name].alias: # type: ignore
            fields_name.append(alias)
        
        for field in fields_name:
            cls.__extended_fields_type__[field].append(new_type)
        
        field_annotation = cls.__annotations__[field_name]
        cls.__annotations__[field_name] = Union[new_type, *field_annotation.__args__]
        
    @model_validator(mode="before")
    @classmethod
    def __validate_model_with_extended_fields(cls, data: Any) -> Any:
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
