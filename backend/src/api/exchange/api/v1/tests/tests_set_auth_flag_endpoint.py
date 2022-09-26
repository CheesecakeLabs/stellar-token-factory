import json

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction

from .mocks.constants import UPDATE_AUTH_FLAG_FAIL_RESPONSES


def post_set_auth_flag_request(
    client: Client, network: str = None, **kwargs
) -> Response:
    """
    Make a request to set auth flag
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:set-auth-flag"),
        data=json.dumps(kwargs),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize(
    "request_data,network",
    (
        (
            {
                "issuer": Keypair().public_key,
                "target": Keypair().public_key,
                "asset_code": "TKN",
            },
            "TESTNET",
        ),
        (
            {
                "issuer": Keypair().public_key,
                "target": Keypair().public_key,
                "asset_code": "TKN",
                "memo_text": "Some memo",
            },
            "PUBLIC",
        ),
    ),
)
def test_set_auth_flag_successfully(
    mocker: MockerFixture, client: Client, request_data: dict, network: str
) -> None:
    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=request_data["issuer"],
            ),
            get_mocked_account_object(
                account_id=request_data["target"],
            ),
        ],
    )

    response = post_set_auth_flag_request(
        client=client, network=network, **request_data
    )

    assert load_account_mock.call_count == 2

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json.get("required_signatures")
    assert type(response_json.get("required_signatures")) == list

    assert response_json.get("envelope_xdr")
    assert type(response_json.get("envelope_xdr")) == str

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response_json.get("envelope_xdr")
    )
    assert envelope.transaction.operations[0].set_flags


@pytest.mark.parametrize("request_data,error", UPDATE_AUTH_FLAG_FAIL_RESPONSES)
def test_set_auth_flag_fails_when_request_data_is_wrong(
    client: Client, request_data: dict, error: dict
):
    response = post_set_auth_flag_request(client, **request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error
