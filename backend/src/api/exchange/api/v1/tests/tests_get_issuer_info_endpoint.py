from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response
from stellar_sdk.exceptions import NotFoundError

from api.exchange.use_cases.tests.mocks import constants
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def get_issuer_info_request(
    client: Client,
    public_key: str,
    network: str = None,
) -> Response:
    """
    Make a request to list issued assets
    Args:
        client: HTTP Client
        public_key: Wallet public key
    Returns: Wallet issued assets
    """
    return client.get(
        path=reverse("exchange:get-issuer-info", kwargs={"public_key": public_key}),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_get_issuer_info_successfully(
    client: Client, mocker: MockerFixture, network: str
) -> None:
    public_key: str = Keypair().public_key

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=public_key),
    )

    get_assets_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.call",
        return_value=constants.STELLAR_ASSETS_RESPONSE,
    )

    next_assets_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.next",
        return_value=constants.STELLAR_ASSETS_EMPTY_RESPONSE,
    )

    response = get_issuer_info_request(
        client=client, network=network, public_key=public_key
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "clawback": True,
        "freeze": True,
        "assets": [
            {
                "code": "RIO",
                "issuer": "GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
                "supply": 922337203685.47,
                "name": "RIO-GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
            },
            {
                "code": "USD",
                "issuer": "GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
                "supply": 922337203685.47,
                "name": "USD-GC4MQOLFBOGBZ4GBNF7K7E56QUKNNX3BD4VREWMPDPHHUCABFNRS2A23",
            },
        ],
    }

    load_account_mock.assert_called_once()
    get_assets_mock.assert_called_once()
    next_assets_mock.assert_called_once()


def test_get_issuer_info_with_invalid_public_key(client: Client) -> None:
    public_key = "invalid-key"

    response = get_issuer_info_request(client=client, public_key=public_key)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"code": 1, "detail": "invalid_public_key"}


def test_get_issuer_info_with_account_does_not_exists(
    client: Client, mocker: MockerFixture
) -> None:
    public_key: str = Keypair().public_key

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=NotFoundError(
            ResponseMock(
                text="NotFoundError",
                status_code=status.HTTP_400_BAD_REQUEST,
                json=lambda: constants.STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
            )
        ),
    )

    response = get_issuer_info_request(client=client, public_key=public_key)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"code": 2, "detail": "account_not_found"}

    load_account_mock.assert_called_once()
