from copy import deepcopy

import pytest

from alice_types import request
import schemes


@pytest.fixture()
def override_state_field():
    old_model = deepcopy(request.State)

    request.State.extend_session_model(schemes.SessionState)
    request.State.extend_user_model(schemes.UserState)

    yield

    request.State = old_model


@pytest.fixture()
def override_purchase_payload_request_field():
    old_model = deepcopy(request.RequestPurchase)
    request.RequestPurchase.extend_payload_model(schemes.PurchasePayload)

    yield

    request.RequestPurchase = old_model
