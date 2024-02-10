from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from alice_types import request


class PurchasePayload(BaseModel):
    id: str = Field(...)
    status: str = Field(...)
    paid: bool = Field(...)
    amount: Decimal = Field(...)
    currency: Optional[str] = Field(default="RUB")


request.RequestPurchase.extend_payload_model(PurchasePayload)

data = {
    "type": "Purchase.Confirmation",
    "purchase_request_id": "d432de19be8347d09f656d9fe966e2f9",
    "purchase_token": "d432de19be8347d09f656d9fe966e2f9",
    "order_id": "eeb59d64-9e6a-11ea-bb37-0242ac130002",
    "purchase_timestamp": 1590399311,
    "purchase_payload": {
        "id": "22c5d173-000f-5000-9000-1bdf241d4651",
        "status": "wait",
        "paid": False,
        "amount": "5",
        "currency": "USD",
    },
    "signed_data": "purchase_request_id=id_value&purchase_token=token_value&order_id=id_value&...",
    "signature": "Pi6JNCFeeleRa...",
}

purchase = request.RequestPurchase.model_validate(data)
payload = purchase.payload
assert isinstance(payload, PurchasePayload)
assert all([
    payload.status == "wait",
    payload.paid is False,
])
