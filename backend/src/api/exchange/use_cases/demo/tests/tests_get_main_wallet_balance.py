from collections import namedtuple

import pytest
from django.test import override_settings
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases.demo import GetMainWalletBalance
from api.exchange.use_cases.tests.mocks.constants import (
    STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
)
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

from .mocks import constants

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


@pytest.mark.parametrize(
    "asset_code,asset_issuer,balance",
    (
        (
            "EUR",
            "GC3XSOYSQDYBBGBBMV7OBZJOZQL47POSV6R4WPPXQVYMIEQBDFTAK46U",
            "10000000000.0000000",
        ),
        (
            "USD",
            "GDGDATWYNYC5SBZORXK3JVU5NSIHSZWB72FWCBWYCQIMYS5V3BUK4PH7",
            "10.0000000",
        ),
    ),
)
@override_settings(
    MAIN_WALLET_PK="GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ"
)
def test_main_wallet_balance_succesfully(
    mocker: MockerFixture, asset_code: str, asset_issuer: str, balance: str
):
    network = "TESTNET"

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(data=constants.STELLAR_ACCOUNT_RESPONSE),
    )

    response: list = GetMainWalletBalance().execute(
        network=network, asset_code=asset_code, asset_issuer=asset_issuer
    )

    load_account_mock.assert_called_with(
        "GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ"
    )
    acc_get_network_data_mock.assert_called_with(network)

    assert response == {
        "balance": balance,
        "limit": "922337203685.4775807",
        "buying_liabilities": "0.0000000",
        "selling_liabilities": "0.0000000",
        "last_modified_ledger": 659249,
        "is_authorized": True,
        "is_authorized_to_maintain_liabilities": True,
        "asset_type": "credit_alphanum4",
        "asset_code": asset_code,
        "asset_issuer": asset_issuer,
    }


@override_settings(MAIN_WALLET_PK="invalid-key")
def test_get_issuer_info_fails_when_public_key_is_invalid(mocker: MockerFixture):
    data = {
        "network": "TESTNET",
        "asset_code": "EUR",
        "asset_issuer": Keypair().public_key,
    }

    with pytest.raises(
        BusinessException,
        match="{'code': 1, 'detail': 'invalid_public_key'}",
    ):
        GetMainWalletBalance().execute(**data)


@override_settings(
    MAIN_WALLET_PK="GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ"
)
def test_get_issuer_info_fails_when_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "asset_code": "EUR",
        "asset_issuer": Keypair().public_key,
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=NotFoundError(
            ResponseMock(
                text="NotFoundError",
                status_code=status.HTTP_404_NOT_FOUND,
                json=lambda: STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
            )
        ),
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 2, 'detail': 'account_not_found'}",
    ):
        GetMainWalletBalance().execute(**data)

    load_account_mock.assert_called_with(
        "GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ"
    )


def test_get_issuer_info_fails_when_network_is_invalid():
    data = {
        "network": "invalid",
        "asset_code": "EUR",
        "asset_issuer": Keypair().public_key,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        GetMainWalletBalance().execute(**data)
