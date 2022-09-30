from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.create_claimable_balance import CreateClaimableBalance
from stellar_sdk.operation.payment import Payment

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import CreatePaymentUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_create_payment_fails_when_issuer_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": "invalid-key",
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        CreatePaymentUseCase().execute(**data)


def test_create_payment_fails_when_distributor_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": "invalid-key",
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 4, 'detail': 'invalid_distributor_public_key'}",
    ):
        CreatePaymentUseCase().execute(**data)


def test_create_payment_fails_when_target_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "target": "invalid-key",
        "asset_code": "TKN",
        "amount": 10,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 10, 'detail': 'invalid_target_public_key'}",
    ):
        CreatePaymentUseCase().execute(**data)


def test_create_payment_fails_when_issuer_is_the_target():
    issuer_key: str = Keypair().public_key
    data = {
        "network": "TESTNET",
        "issuer": issuer_key,
        "distributor": Keypair().public_key,
        "target": issuer_key,
        "asset_code": "TKN",
        "amount": 10,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 12, 'detail': 'issuer_cannot_be_the_target'}",
    ):
        CreatePaymentUseCase().execute(**data)


def test_create_payment_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        CreatePaymentUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_create_payment_fails_when_distributor_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
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
        CreatePaymentUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_with(data["distributor"])


def test_create_payment_fails_when_issuer_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
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
        CreatePaymentUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    assert load_account_mock.call_count == 2


def test_create_payment_fails_when_target_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
    }
    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["distributor"]),
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
        match="{'code': 11, 'detail': 'target_account_not_found'}",
    ):
        CreatePaymentUseCase().execute(**data)

    assert load_account_mock.call_count == 3


@pytest.mark.parametrize(
    "asset_code,issuer,has_trustline,network",
    (
        (
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            True,
            "TESTNET",
        ),
        ("ANOTHERTKN", Keypair().public_key, False, "TESTNET"),
        (
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            True,
            "PUBLIC",
        ),
        ("ANOTHERTKN", Keypair().public_key, False, "PUBLIC"),
    ),
)
def test_create_payment_succesfully(
    mocker: MockerFixture,
    asset_code: str,
    issuer: str,
    has_trustline: bool,
    network: str,
):
    data = {
        "network": network,
        "issuer": issuer,
        "distributor": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": asset_code,
        "amount": 10,
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
            get_mocked_account_object(
                account_id=data["target"],
            ),
        ],
    )

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    response: dict = CreatePaymentUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    acc_get_network_data_mock.assert_called_with(network)
    assert load_account_mock.call_count == 3

    assert response.get("required_signatures") == set([data.get("distributor")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    if has_trustline:
        # Payment operation
        assert type(envelope.transaction.operations[0]) == Payment
        assert (
            envelope.transaction.operations[0].source.account_id == data["distributor"]
        )
        assert (
            envelope.transaction.operations[0].destination.account_id == data["target"]
        )
        assert envelope.transaction.operations[0].amount == str(data["amount"])
        assert envelope.transaction.operations[0].asset.code == data["asset_code"]
        assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
    else:
        # Create Claimable Balance operation
        assert type(envelope.transaction.operations[0]) == CreateClaimableBalance
        assert (
            envelope.transaction.operations[0].source.account_id == data["distributor"]
        )
        assert len(envelope.transaction.operations[0].claimants) == 1
        assert (
            envelope.transaction.operations[0].claimants[0].destination
            == data["target"]
        )
        assert envelope.transaction.operations[0].amount == str(data["amount"])
        assert envelope.transaction.operations[0].asset.code == data["asset_code"]
        assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
