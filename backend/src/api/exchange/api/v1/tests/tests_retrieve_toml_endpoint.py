import copy
from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.api.v1 import messages
from api.exchange.use_cases.tests.mocks import constants
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair

from .mocks.constants import RETRIEVE_TOML_ENDPOINT_RESPONSE

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def retrieve_toml_request(
    client: Client,
    asset_issuer: str,
    network: str = None,
) -> Response:
    """
    Make a request to retrieve TOML
    Args:
        client: HTTP Client
        asset_issuer: Asset issuer public key
    """
    return client.get(
        path=reverse(
            "exchange:retrieve-toml",
            kwargs={"asset_issuer": asset_issuer},
        ),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_retrieve_toml_request_successfully(
    client: Client, mocker: MockerFixture, network: str
) -> None:
    public_key: str = Keypair().public_key

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=public_key),
    )

    fetch_stellar_toml_mock = mocker.patch(
        "stellar_sdk.sep.stellar_toml.fetch_stellar_toml",
        return_value=copy.deepcopy(constants.FETCH_STELLAR_TOML_RESPONSE),
    )

    response = retrieve_toml_request(
        client=client, network=network, asset_issuer=public_key
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == RETRIEVE_TOML_ENDPOINT_RESPONSE

    load_account_mock.assert_called_once()
    fetch_stellar_toml_mock.assert_called_once()


def test_retrieve_toml_request_not_found(client: Client, mocker: MockerFixture) -> None:
    public_key: str = Keypair().public_key

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=public_key),
    )

    fetch_stellar_toml_mock = mocker.patch(
        "stellar_sdk.sep.stellar_toml.fetch_stellar_toml",
        side_effect=ConnectionError(),
    )

    response = retrieve_toml_request(
        client=client, network="TESTNET", asset_issuer=public_key
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    load_account_mock.assert_called_once()
    fetch_stellar_toml_mock.assert_called_once()
