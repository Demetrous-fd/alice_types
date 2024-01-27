from typing import Type, Union
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, SerializeAsAny, field_serializer

from alice_types.mixin import DynamicFieldsTypeMixin


class RequestPurchaseType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
    PURCHASE_CONFIRMATION = "Purchase.Confirmation"


# https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
class RequestPurchase(BaseModel, DynamicFieldsTypeMixin):
    type: RequestPurchaseType = Field(...)
    request_id: str = Field(..., alias="purchase_request_id")
    token: str = Field(..., alias="purchase_token")
    order_id: str = Field(...)
    timestamp: datetime = Field(..., alias="purchase_timestamp")
    payload: SerializeAsAny[Union[dict, BaseModel]] = Field(alias="purchase_payload")
    signed_data: str = Field(...)  # TODO: validation: purchase_request_id=[value]&purchase_token=[value]&order_id=[value]&purchase_timestamp=[value]
    signature: str = Field(...)

    @classmethod
    def extend_payload_model(cls, model: Type[BaseModel]):
        cls.extend_field_type("payload", model)

    @field_serializer("timestamp")
    def serialize_timestamp(self, value: datetime) -> int:
        return int(value.timestamp())
