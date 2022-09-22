import copy
from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import GetAccountOptionsUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_get_account_options_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "public_key": Keypair().public_key,
    }

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        GetAccountOptionsUseCase().execute(**data)

    acc_get_network_data_mock.assert_called_with(data.get("network"))


def test_get_account_options_fails_when_public_key_is_invalid():
    data = {"network": "TESTNET", "public_key": "invalid-key"}
    with pytest.raises(
        BusinessException,
        match="{'code': 1, 'detail': 'invalid_public_key'}",
    ):
        GetAccountOptionsUseCase().execute(**data)


def test_get_account_options_fails_when_account_not_found(
    mocker: MockerFixture,
):
    data = {"network": "TESTNET", "public_key": Keypair().public_key}

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=NotFoundError(
            ResponseMock(
                text="NotFoundError",
                status_code=status.HTTP_404_NOT_FOUND,
                json=lambda: constants.STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
            )
        ),
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 2, 'detail': 'account_not_found'}",
    ):
        GetAccountOptionsUseCase().execute(**data)

    load_account_mock.assert_called_with(data.get("public_key"))


@pytest.mark.parametrize(
    "network,clawback,freeze",
    (
        ("TESTNET", True, True),
        ("TESTNET", False, True),
        ("TESTNET", False, False),
        ("PUBLIC", True, True),
        ("PUBLIC", False, True),
        ("PUBLIC", False, False),
    ),
)
def test_get_account_options_succesfully(
    mocker: MockerFixture, network: str, clawback: bool, freeze: bool
):
    public_key = "GBJTVOA6OAOAMFUBBBG2S4Z54IM5YQB34SVZFUX6MP72I745YATR6WLT"

    account_data = copy.deepcopy(constants.STELLAR_ACCOUNT_RESPONSE)
    account_data["signers"][1]["weight"] = 1
    account_data["flags"]["auth_revocable"] = freeze
    account_data["flags"]["auth_clawback_enabled"] = clawback

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(
            account_id=public_key, data=account_data
        ),
    )

    response: list = GetAccountOptionsUseCase().execute(
        network=network, public_key=public_key
    )

    load_account_mock.assert_called_once()
    acc_get_network_data_mock.assert_called_with(network)

    assert response == {
        "clawback": clawback,
        "freeze": freeze,
        "signers": ["GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC"],
    }
