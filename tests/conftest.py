from copy import deepcopy

import pytest

import alice_types
import schemes


@pytest.fixture()
def override_state_field():
    old_model = deepcopy(alice_types.State)

    alice_types.State.extend_session_model(schemes.SessionState)
    alice_types.State.extend_user_model(schemes.UserState)

    yield

    alice_types.State = old_model


@pytest.fixture()
def override_purchase_payload_request_field():
    old_model = deepcopy(alice_types.request.RequestPurchase)
    alice_types.request.RequestPurchase.extend_payload_model(schemes.PurchasePayload)

    yield

    alice_types.request.RequestPurchase = old_model
