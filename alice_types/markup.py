from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Markup(BaseModel):
    dangerous_context: Optional[bool] = Field(
        default=None,
        description="Признак реплики, которая содержит криминальный подтекст (самоубийство, разжигание ненависти, угрозы)."
    )
