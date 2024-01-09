from typing import Type, ClassVar, List, Any
from collections import defaultdict

from pydantic import BaseModel, model_validator, ValidationError, model_serializer


class AvailableMixin:
    def available(self) -> List[str]:
        available = []
        for name, value in self.__dict__.items():
            if value is not None:
                available.append(name)
        
        return available


class ExcludeUnsetMixin:
    @model_serializer
    def _serialize(self) -> dict:
        __exclude_if_unset__ = set()

        data = dict()
        for field_name, field_info in self.model_fields.items():
            if field_info.json_schema_extra is not None:
                if field_info.json_schema_extra.get("exclude_unset", False):
                    __exclude_if_unset__.add(field_name)

        __exclude_if_unset__.difference_update(self.model_fields_set)

        for field, value in self:
            if field not in __exclude_if_unset__:
                data[field] = value
        return data


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
        
        field_annotation.__args__ = (new_type, *field_annotation.__args__)
        cls.__annotations__[field_name] = field_annotation
        
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
