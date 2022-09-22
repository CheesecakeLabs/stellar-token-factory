from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.api.v1 import messages
from api.exchange.use_cases.tests.mocks import constants

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def get_asset_distributor_request(
    client: Client,
    asset_code: str,
    asset_issuer: str,
    network: str = None,
) -> Response:
    """
    Make a request to list issued assets
    Args:
        client: HTTP Client
        asset_code: Asset code
        asset_issuer: Asset issuer public key
    Returns: Wallet issued assets
    """
    return client.get(
        path=reverse(
            "exchange:get-asset-distributor",
            kwargs={"asset_code": asset_code, "asset_issuer": asset_issuer},
        ),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_get_asset_distributor_request_successfully(
    client: Client, mocker: MockerFixture, network: str
) -> None:
    asset_data = {
        "asset_code": "USDC",
        "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
    }

    call_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.call",
        side_effect=[constants.STELLAR_GET_PAYMENTS_RESPONSE],
    )

    response = get_asset_distributor_request(
        client=client, network=network, **asset_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "public_key": "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU"
    }

    call_mock.assert_called_once()


def test_get_asset_distributor_request_not_found(
    client: Client, mocker: MockerFixture
) -> None:
    asset_data = {
        "asset_code": "USDC",
        "asset_issuer": "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
    }

    call_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.call",
        side_effect=[
            constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
            constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
        ],
    )
    next_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.next",
        side_effect=[
            constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
        ],
    )

    response = get_asset_distributor_request(client=client, **asset_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == messages.DISTRIBUTOR_NOT_FOUND

    call_mock.num_called
    next_mock.assert_called_once()
