from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.change_trust import ChangeTrust

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import CreateAssetUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")

LIMIT_MAX_VALUE = 922337203685.4775


def test_create_asset_fails_when_issuer_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": "invalid-key",
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        CreateAssetUseCase().execute(**data)


def test_create_asset_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        CreateAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_create_asset_fails_when_distributor_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": "invalid-key",
        "asset_code": "TKN",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 4, 'detail': 'invalid_distributor_public_key'}",
    ):
        CreateAssetUseCase().execute(**data)


def test_create_asset_fails_when_distributor_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
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
        match="{'code': 6, 'detail': 'distributor_account_not_found'}",
    ):
        CreateAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_with(data["distributor"])


def test_create_asset_fails_when_issuer_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["distributor"]),
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
        match="{'code': 5, 'detail': 'issuer_account_not_found'}",
    ):
        CreateAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.call_count == 2


@pytest.mark.parametrize(
    "limit,network",
    (
        (None, "TESTNET"),
        (10000, "TESTNET"),
        (10.4, "TESTNET"),
        (0, "TESTNET"),
        (None, "PUBLIC"),
        (10000, "PUBLIC"),
        (10.4, "PUBLIC"),
        (0, "PUBLIC"),
    ),
)
def test_create_asset_succesfully(mocker: MockerFixture, limit: float, network: str):
    data = {
        "network": network,
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "asset_code": "TKN",
        "limit": limit,
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=data["distributor"],
            ),
            get_mocked_account_object(
                account_id=data["issuer"],
            ),
        ],
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    response: dict = CreateAssetUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)

    load_account_mock.call_count == 2

    assert response.get("required_signatures") == set([data.get("distributor")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    # Change Trust operation
    assert type(envelope.transaction.operations[0]) == ChangeTrust
    assert envelope.transaction.operations[0].source.account_id == data["distributor"]
    assert envelope.transaction.operations[0].asset.code == data["asset_code"]
    assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
    assert float(envelope.transaction.operations[0].limit) == (
        data["limit"] if data["limit"] is not None else LIMIT_MAX_VALUE
    )
