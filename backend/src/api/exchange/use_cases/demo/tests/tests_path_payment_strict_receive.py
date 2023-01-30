from collections import namedtuple

import pytest
from django.test import override_settings
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.path_payment_strict_receive import PathPaymentStrictReceive
from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases.demo import CreatePathPaymentStrictReceiveUseCase
from api.exchange.use_cases.tests.mocks import constants
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")

EUR_CODE = "EUR"
USD_CODE = "USD"
MAIN_WALLET = Keypair()
EUR_ISSUER = Keypair()
USD_ISSUER = Keypair()

SETTINGS_DATA = {
    "MAIN_WALLET_PK": MAIN_WALLET.public_key,
    "EUR_CODE": EUR_CODE,
    "USD_CODE": USD_CODE,
    "EUR_ISSUER": EUR_ISSUER.public_key,
    "USD_ISSUER": USD_ISSUER.public_key,
    "EUR_PRICE": 0.90909091,
    "USD_PRICE": 1.1,
    "USERS": {
        "user1": (Keypair().secret, 2),
        "user2": (Keypair().secret, 1),
        "user3": (Keypair().secret, 1),
    }
}

@override_settings(
    **SETTINGS_DATA
)
def test_create_path_payment_fails_when_user_not_found():
    data = {
        "network": "TESTNET",
        "destination_public_key": Keypair().public_key,
        "receive_amount": 10.0,
        "user_id": "user4",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 22, 'detail': 'user_not_found'}",
    ):
        CreatePathPaymentStrictReceiveUseCase().execute(**data)

@override_settings(
    **SETTINGS_DATA
)
def test_create_path_payment_fails_when_dest_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "destination_public_key": "invalid-key",
        "receive_amount": 10.0,
        "user_id": "user1",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 10, 'detail': 'invalid_target_public_key'}",
    ):
        CreatePathPaymentStrictReceiveUseCase().execute(**data)

@override_settings(
    **SETTINGS_DATA
)
def test_create_path_payment_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "destination_public_key": Keypair().public_key,
        "receive_amount": 10.0,
        "user_id": "user1",
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        CreatePathPaymentStrictReceiveUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


@override_settings(
    **SETTINGS_DATA
)
def test_create_path_payment_fails_when_main_wallet_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "destination_public_key": Keypair().public_key,
        "receive_amount": 10.0,
        "user_id": "user1",
    }

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
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 2, 'detail': 'account_not_found'}",
    ):
        CreatePathPaymentStrictReceiveUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_with(MAIN_WALLET.public_key)


@override_settings(
    **SETTINGS_DATA
)
def test_create_path_payment_fails_when_destination_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "destination_public_key": Keypair().public_key,
        "receive_amount": 10.0,
        "user_id": "user1",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=MAIN_WALLET.public_key),
            NotFoundError(
                ResponseMock(
                    text="NotFoundError",
                    status_code=status.HTTP_404_NOT_FOUND,
                    json=lambda: constants.STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
                )
            ),
        ],
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 11, 'detail': 'target_account_not_found'}",
    ):
        CreatePathPaymentStrictReceiveUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    assert load_account_mock.call_count == 2


@override_settings(
    **SETTINGS_DATA
)
@pytest.mark.parametrize("user_id", ("user1", "user2", "user3"))
def test_create_path_payment_succesfully(mocker: MockerFixture, user_id: str):
    data = {
        "network": "TESTNET",
        "destination_public_key": Keypair().public_key,
        "receive_amount": 10,
        "user_id": user_id,
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=MAIN_WALLET.public_key,
            ),
            get_mocked_account_object(
                account_id=data["destination_public_key"],
            ),
        ],
    )

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    response: dict = CreatePathPaymentStrictReceiveUseCase().execute(**data)

    get_network_data_mock.assert_called_with("TESTNET")
    assert load_account_mock.call_count == 2

    assert response.get("final_cost") == 9.1
    assert response.get("usd_price") == 1.1

    match user_id:
        case "user1":
            assert response.get("required_signatures") == []
        case "user2":
            assert response.get("required_signatures") == ["user3"]
        case "user3":
            assert response.get("required_signatures") == ["user2"]


    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 1

    # Payment operation
    assert type(envelope.transaction.operations[0]) == PathPaymentStrictReceive
    assert (
        envelope.transaction.operations[0].source.account_id == MAIN_WALLET.public_key
    )
    assert (
        envelope.transaction.operations[0].destination.account_id
        == data["destination_public_key"]
    )
    assert envelope.transaction.operations[0].dest_amount == str(data["receive_amount"])
    assert envelope.transaction.operations[0].send_max == str(9.1)
    assert envelope.transaction.operations[0].path == []
    assert envelope.transaction.operations[0].dest_asset.code == USD_CODE
    assert envelope.transaction.operations[0].dest_asset.issuer == USD_ISSUER.public_key
    assert envelope.transaction.operations[0].send_asset.code == EUR_CODE
    assert envelope.transaction.operations[0].send_asset.issuer == EUR_ISSUER.public_key
