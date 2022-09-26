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

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")
from .mocks.constants import MINT_ASSET_FAIL_RESPONSES


def post_mint_asset_request(client: Client, network: str = None, **kwargs) -> Response:
    """
    Make a request to mint asset
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:mint-asset"),
        data=json.dumps(kwargs),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_mint_asset_successfully(
    mocker: MockerFixture, client: Client, network: str
) -> None:

    request_data = {
        "issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 300,
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=request_data["distributor"],
            ),
            get_mocked_account_object(
                account_id=request_data["issuer"],
            ),
        ],
    )

    response = post_mint_asset_request(client=client, network=network, **request_data)

    assert load_account_mock.call_count == 2

    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()

    assert response_json.get("required_signatures")
    assert type(response_json.get("required_signatures")) == list

    assert response_json.get("envelope_xdr")
    assert type(response_json.get("envelope_xdr")) == str


@pytest.mark.parametrize("request_data,error", MINT_ASSET_FAIL_RESPONSES)
def test_mint_asset_fails_when_request_data_is_wrong(
    client: Client, request_data: dict, error: dict
):

    response = post_mint_asset_request(client, **request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error
