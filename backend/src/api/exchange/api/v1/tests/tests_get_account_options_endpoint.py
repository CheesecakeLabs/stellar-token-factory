from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.use_cases.tests.mocks import constants
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def get_account_options_request(
    client: Client,
    public_key: str,
    network: str = None,
) -> Response:
    """
    Make a request to get account options
    Args:
        client: HTTP Client
        public_key: Wallet public key
    """
    return client.get(
        path=reverse("exchange:get-account-options", kwargs={"public_key": public_key}),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_get_account_options_successfully(
    client: Client, mocker: MockerFixture, network: str
) -> None:
    public_key: str = Keypair().public_key

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=public_key),
    )

    response = get_account_options_request(
        client=client, network=network, public_key=public_key
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "clawback": True,
        "freeze": True,
        "signers": ["GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC"],
    }

    load_account_mock.assert_called_once()
