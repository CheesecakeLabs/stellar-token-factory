import json
from collections import namedtuple

import pytest
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair
from django.test import override_settings
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")
from .mocks.constants import CREATE_PATH_PAYMENT_FAIL_RESPONSES

EUR_CODE = "EUR"
USD_CODE = "USD"
MAIN_WALLET = Keypair()
EUR_ISSUER = Keypair()
USD_ISSUER = Keypair()


def post_create_path_payment_request(client: Client, **kwargs) -> Response:
    """
    Make a request to create a path payment strict receive envelope
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:path-payment-strict-receive"),
        data=json.dumps(kwargs),
        content_type="application/json",
    )


@override_settings(
    MAIN_WALLET_PK=MAIN_WALLET.public_key,
    EUR_CODE=EUR_CODE,
    USD_CODE=USD_CODE,
    EUR_ISSUER=EUR_ISSUER.public_key,
    USD_ISSUER=USD_ISSUER.public_key,
)
def test_create_path_payment_successfully(
    mocker: MockerFixture, client: Client
) -> None:

    request_data = {
        "destination_public_key": Keypair().public_key,
        "receive_amount": 500,
        "user_id": "user2",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=MAIN_WALLET.public_key,
            ),
            get_mocked_account_object(
                account_id=request_data["destination_public_key"],
            ),
        ],
    )

    response = post_create_path_payment_request(client=client, **request_data)

    assert load_account_mock.call_count == 2

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json.get("final_cost")
    assert type(response_json.get("final_cost")) == float

    assert response_json.get("envelope_xdr")
    assert type(response_json.get("envelope_xdr")) == str

    assert response_json.get("required_signatures")
    assert type(response_json.get("required_signatures")) == list

    assert response_json.get("usd_price")
    assert type(response_json.get("usd_price")) == float


@pytest.mark.parametrize("request_data,error", CREATE_PATH_PAYMENT_FAIL_RESPONSES)
def test_create_payment_fails_when_request_data_is_wrong(
    client: Client, request_data: dict, error: dict
):
    response = post_create_path_payment_request(client, **request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error
