from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RequestPurchaseType(str, Enum):
    # https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
    PURCHASE_CONFIRMATION = "Purchase.Confirmation"


# https://yandex.ru/dev/dialogs/alice/doc/request-purchase-confirmation.html
class RequestPurchase(BaseModel):
    type: RequestPurchaseType = Field(...)
    purchase_request_id: str = Field(...)
    purchase_token: str = Field(...)
    order_id: str = Field(...)
    purchase_timestamp: datetime = Field(...)
    purchase_payload: dict = Field(...)
    signed_data: str = Field(...)  # TODO: validation
    signature: str = Field(...)
