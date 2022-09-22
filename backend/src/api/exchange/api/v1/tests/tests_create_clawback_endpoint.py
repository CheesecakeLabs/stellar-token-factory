import json
from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair

from .mocks.constants import CREATE_CLAWBACK_FAIL_RESPONSES

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def post_create_clawback_request(
    client: Client, network: str = None, **kwargs
) -> Response:
    """
    Make a request to create a Clawback operation
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:create-clawback"),
        data=json.dumps(kwargs),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize(
    "request_data,network",
    (
        (
            {
                "issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
                "target": Keypair().public_key,
                "asset_code": "TKN",
                "amount": 103.89,
                "claimable_id": None,
            },
            "TESTNET",
        ),
        (
            {
                "issuer": Keypair().public_key,
                "claimable_id": "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
            },
            "PUBLIC",
        ),
    ),
)
def test_create_clawback_successfully(
    mocker: MockerFixture, client: Client, request_data: dict, network: str
) -> None:

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=request_data["issuer"],
            ),
            get_mocked_account_object(
                account_id=request_data.get("target"),
            ),
        ],
    )

    response = post_create_clawback_request(
        client=client, network=network, **request_data
    )

    load_account_mock.call_count == 1 + bool(request_data.get("target"))

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json.get("required_signatures")
    assert type(response_json.get("required_signatures")) == list

    assert response_json.get("envelope_xdr")
    assert type(response_json.get("envelope_xdr")) == str


@pytest.mark.parametrize("request_data,error", CREATE_CLAWBACK_FAIL_RESPONSES)
def test_create_clawback_fails_when_request_data_is_wrong(
    client: Client, request_data: dict, error: dict
):
    response = post_create_clawback_request(client, **request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error
