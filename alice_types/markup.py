from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Markup(BaseModel):
    dangerous_context: Optional[bool] = Field(
        default=None,
        description="Признак реплики, которая содержит криминальный подтекст (самоубийство, разжигание ненависти, угрозы)." \
                    "Возможно только значение true."
    )
    
    @model_validator(mode="after") # type: ignore
    def validate_dangerous_context(self) -> "Markup":
        if self.dangerous_context is False:
            raise ValueError("Поле dangerous_context может иметь только значение true. Если признак не применим, это свойство не включается в ответ.")
        return self
