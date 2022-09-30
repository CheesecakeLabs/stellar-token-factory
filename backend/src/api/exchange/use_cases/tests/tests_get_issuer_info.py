import copy
from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import GetIssuerInfoUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_get_issuer_info_fails_when_public_key_is_invalid(mocker: MockerFixture):
    data = {"network": "TESTNET", "public_key": "invalid-key"}

    with pytest.raises(
        BusinessException,
        match="{'code': 1, 'detail': 'invalid_public_key'}",
    ):
        GetIssuerInfoUseCase().execute(**data)


def test_get_issuer_info_fails_when_account_not_found(
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
        GetIssuerInfoUseCase().execute(**data)

    load_account_mock.assert_called_with(data.get("public_key"))


def test_get_issuer_info_fails_when_network_is_invalid():
    data = {"network": "invalid", "public_key": Keypair().public_key}
    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        GetIssuerInfoUseCase().execute(**data)


@pytest.mark.parametrize(
    "network,accounts_call_return_value,accounts_next_side_effect,assets_call_side_effect,assets_next_side_effect,freeze,clawback",
    (
        (
            "TESTNET",
            constants.STELLAR_GET_ACCOUNTS_ONE_ACCOUNT_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [constants.STELLAR_ASSETS_RESPONSE],
            [constants.STELLAR_ASSETS_EMPTY_RESPONSE],
            True,
            True,
        ),
        (
            "PUBLIC",
            constants.STELLAR_GET_ACCOUNTS_ONE_ACCOUNT_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [constants.STELLAR_ASSETS_RESPONSE],
            [
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            True,
            False,
        ),
        (
            "TESTNET",
            constants.STELLAR_GET_ACCOUNTS_ONE_ACCOUNT_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [constants.STELLAR_ASSETS_EMPTY_RESPONSE],
            [constants.STELLAR_ASSETS_EMPTY_RESPONSE],
            False,
            False,
        ),
        (
            "PUBLIC",
            constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            False,
            False,
        ),
        (
            "TESTNET",
            constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            True,
            True,
        ),
        (
            "TESTNET",
            constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            True,
            False,
        ),
        (
            "PUBLIC",
            constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            [constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            True,
            False,
        ),
        (
            "TESTNET",
            constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            [
                constants.STELLAR_GET_ACCOUNTS_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            [
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
                constants.STELLAR_ASSETS_EMPTY_RESPONSE,
            ],
            True,
            True,
        ),
    ),
)
def test_get_issuer_info_succesfully(
    mocker: MockerFixture,
    network: str,
    accounts_call_return_value: dict,
    accounts_next_side_effect: list,
    assets_call_side_effect: list,
    assets_next_side_effect: list,
    freeze: bool,
    clawback: bool,
):
    public_key: str = Keypair().public_key

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    account_data = copy.deepcopy(constants.STELLAR_ACCOUNT_RESPONSE)
    account_data["flags"]["auth_revocable"] = freeze
    account_data["flags"]["auth_clawback_enabled"] = clawback

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(
            account_id=public_key, data=account_data
        ),
    )

    get_accounts_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.accounts_call_builder.AccountsCallBuilder.call",
        return_value=accounts_call_return_value,
    )

    next_accounts_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.accounts_call_builder.AccountsCallBuilder.next",
        side_effect=accounts_next_side_effect,
    )

    get_assets_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.assets_call_builder.AssetsCallBuilder.call",
        side_effect=assets_call_side_effect,
    )

    next_assets_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.assets_call_builder.AssetsCallBuilder.next",
        side_effect=assets_next_side_effect,
    )

    response: list = GetIssuerInfoUseCase().execute(
        network=network, public_key=public_key
    )

    acc_get_network_data_mock.assert_called_with(network)
    load_account_mock.assert_called_once()
    get_accounts_mock.assert_called_once()
    assert next_accounts_mock.call_count == len(accounts_next_side_effect)
    assert get_assets_mock.call_count == len(assets_call_side_effect)
    assert next_assets_mock.call_count == len(assets_next_side_effect)

    expected_response = {
        "clawback": clawback,
        "freeze": freeze,
        "assets": sum(
            [value["_embedded"]["records"] for value in assets_call_side_effect], []
        )
        + sum([value["_embedded"]["records"] for value in assets_next_side_effect], []),
    }

    assert response == expected_response
