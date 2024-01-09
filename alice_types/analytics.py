from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from alice_types.mixin import ExcludeUnsetMixin


def _count_levels(dictionary):
    max_depth = 0
    stack = [(dictionary, 0)]
    
    while stack:
        current_dict, depth = stack.pop()
        max_depth = max(max_depth, depth)
        
        for value in current_dict.values():
            if isinstance(value, dict):
                stack.append((value, depth + 1))  # type: ignore
    
    return max_depth


class AnalyticsEvent(BaseModel, ExcludeUnsetMixin):
    name: str = Field(...)
    value: Optional[dict] = Field(
        default=None,
        json_schema_extra={"exclude_unset": True}
    )
    
    @field_validator("value", mode="before")
    @classmethod
    def validate_value(cls, value):
        if isinstance(value, dict):
            count_levels = _count_levels(value)
            if count_levels > 5:
                raise ValueError(f"Допустимо не более пяти уровней вложенности события. Максимальная: {count_levels}")
        return value
    

class Analytics(BaseModel):
    events: List[AnalyticsEvent] = Field(default_factory=list)
