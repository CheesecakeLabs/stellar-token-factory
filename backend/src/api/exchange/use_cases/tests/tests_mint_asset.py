from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.payment import Payment

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import MintAssetUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_mint_asset_fails_when_issuer_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": "invalid-key",
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 200,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        MintAssetUseCase().execute(**data)


def test_mint_asset_fails_when_distributor_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": "invalid-key",
        "asset_code": "TKN",
        "amount": 200,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 4, 'detail': 'invalid_distributor_public_key'}",
    ):
        MintAssetUseCase().execute(**data)


def test_mint_asset_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 200,
    }
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        MintAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_mint_asset_fails_when_issuer_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 200,
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
    with pytest.raises(
        BusinessException,
        match="{'code': 5, 'detail': 'issuer_account_not_found'}",
    ):
        MintAssetUseCase().execute(**data)

    load_account_mock.assert_called_with(data["issuer"])


def test_mint_asset_fails_when_distributor_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 200,
    }
    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["issuer"]),
            NotFoundError(
                ResponseMock(
                    text="NotFoundError",
                    status_code=status.HTTP_404_NOT_FOUND,
                    json=lambda: constants.STELLAR_ACCOUNT_NOT_FOUND_RESPONSE,
                )
            ),
        ],
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 6, 'detail': 'distributor_account_not_found'}",
    ):
        MintAssetUseCase().execute(**data)

    assert load_account_mock.call_count == 2


def test_mint_asset_fails_when_distributor_account_doesnt_have_trustline(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 200,
    }
    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["issuer"]),
            get_mocked_account_object(account_id=data["distributor"]),
        ],
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 8, 'detail': 'distributor_has_no_trustline'}",
    ):
        MintAssetUseCase().execute(**data)

    assert load_account_mock.call_count == 2


def test_mint_asset_fails_when_distributor_account_doesnt_have_trustline_limit(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 1000000,
    }
    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["issuer"]),
            get_mocked_account_object(account_id=data["distributor"]),
        ],
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 9, 'detail': 'distributor_has_no_trustline_limit'}",
    ):
        MintAssetUseCase().execute(**data)

    assert load_account_mock.call_count == 2


@pytest.mark.parametrize(
    "network,",
    ("TESTNET", "PUBLIC"),
)
def test_mint_asset_succesfully(mocker: MockerFixture, network: str):
    data = {
        "network": network,
        "issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 300,
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=data["issuer"],
            ),
            get_mocked_account_object(
                account_id=data["distributor"],
            ),
        ],
    )

    response: dict = MintAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    acc_get_network_data_mock.assert_called_with(network)
    assert load_account_mock.call_count == 2

    assert response.get("required_signatures") == set([data.get("issuer")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    # Payment operation
    assert type(envelope.transaction.operations[0]) == Payment
    assert envelope.transaction.operations[0].source.account_id == data["issuer"]
    assert envelope.transaction.operations[0].asset.code == data["asset_code"]
    assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
    assert envelope.transaction.operations[0].amount == str(data["amount"])
    assert (
        envelope.transaction.operations[0].destination.account_id == data["distributor"]
    )
