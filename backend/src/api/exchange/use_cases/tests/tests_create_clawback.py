import copy
from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.clawback import Clawback
from stellar_sdk.operation.clawback_claimable_balance import ClawbackClaimableBalance

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import CreateClawbackUseCase
from api.exchange.use_cases.create_clawback import CreateClawbackUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_create_clawback_fails_when_target_and_claimable_id_are_null():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 13, 'detail': 'no_target_selected'}",
    ):
        CreateClawbackUseCase().execute(**data)


@pytest.mark.parametrize(
    "asset_code,amount",
    (
        (None, None),
        ("TKN", None),
        (None, 10),
    ),
)
def test_create_clawback_fails_when_target_data_is_missing(
    asset_code: str, amount: float
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "amount": amount,
        "asset_code": asset_code,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 15, 'detail': 'missing_target_fields'}",
    ):
        CreateClawbackUseCase().execute(**data)


def test_create_clawback_fails_when_issuer_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": "invalid-key",
        "target": Keypair().public_key,
        "amount": 10,
        "asset_code": "TKN",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        CreateClawbackUseCase().execute(**data)


def test_create_clawback_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "INVALID",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "amount": 10,
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
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_create_clawback_fails_when_issuer_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "amount": 10,
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
        match="{'code': 5, 'detail': 'issuer_account_not_found'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_with(data["issuer"])


def test_create_clawback_flag_fails_when_issuer_doesnt_have_auth_clawback_enabled(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "amount": 10,
        "asset_code": "TKN",
    }
    issuer_account_data = copy.deepcopy(constants.STELLAR_ACCOUNT_RESPONSE)
    issuer_account_data["flags"]["auth_clawback_enabled"] = False

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=data["issuer"], data=issuer_account_data
            )
        ],
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 18, 'detail': 'issuer_must_have_auth_clawback_flag'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_once()


def test_create_clawback_fails_when_target_public_key_is_invalid(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": "invalid-key",
        "amount": 10,
        "asset_code": "TKN",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=data["issuer"]),
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 10, 'detail': 'invalid_target_public_key'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_once()


def test_create_clawback_fails_when_issuer_is_the_target(
    mocker: MockerFixture,
):
    public_key: str = Keypair().public_key
    data = {
        "network": "TESTNET",
        "issuer": public_key,
        "target": public_key,
        "amount": 10,
        "asset_code": "TKN",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=data["issuer"]),
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 12, 'detail': 'issuer_cannot_be_the_target'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_once()


def test_create_clawback_fails_when_target_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "amount": 10,
        "asset_code": "TKN",
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
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 11, 'detail': 'target_account_not_found'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    assert load_account_mock.call_count == 2


def test_create_clawback_fails_when_target_has_no_trustline(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "amount": 10,
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(account_id=data["issuer"]),
            get_mocked_account_object(account_id=data["target"]),
        ],
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 14, 'detail': 'target_has_no_trustline'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    assert load_account_mock.call_count == 2


def test_create_clawback_fails_when_claimable_id_is_invalid(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "claimable_id": "invalid-id",
    }

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=data["issuer"]),
    )
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 17, 'detail': 'invalid_claimable_id'}",
    ):
        CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))
    load_account_mock.assert_called_once()


@pytest.mark.parametrize(
    "target,asset_code,amount,claimable_id,network",
    (
        (Keypair().public_key, "TKN", 10, None, "TESTNET"),
        (
            Keypair().public_key,
            "TKN",
            10,
            "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
            "TESTNET",
        ),
        (
            None,
            None,
            None,
            "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
            "TESTNET",
        ),
        (Keypair().public_key, "TKN", 10, None, "PUBLIC"),
        (
            Keypair().public_key,
            "TKN",
            10,
            "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
            "PUBLIC",
        ),
        (
            None,
            None,
            None,
            "0000000021397a7e40986f05e43ede59a47b00c3c9ffad75da5065be3a95868c23c06a55",
            "PUBLIC",
        ),
    ),
)
def test_create_clawback_succesfully(
    mocker: MockerFixture,
    asset_code: str,
    target: str,
    amount: float,
    claimable_id: str,
    network: str,
):
    data = {
        "network": network,
        "issuer": "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
        "target": target,
        "asset_code": asset_code,
        "amount": amount,
        "claimable_id": claimable_id,
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
                account_id=data["target"],
            ),
        ],
    )

    response: dict = CreateClawbackUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    acc_get_network_data_mock.assert_called_with(network)
    assert load_account_mock.call_count == 1 + int(bool(target))

    assert response.get("required_signatures") == set([data.get("issuer")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    if target:
        # Clawback operation
        assert type(envelope.transaction.operations[0]) == Clawback
        assert envelope.transaction.operations[0].source.account_id == data["issuer"]
        assert envelope.transaction.operations[0].from_.account_id == data["target"]
        assert envelope.transaction.operations[0].amount == str(data["amount"])
        assert envelope.transaction.operations[0].asset.code == data["asset_code"]
        assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
    else:
        # Clawback Claimable Balance operation
        assert type(envelope.transaction.operations[0]) == ClawbackClaimableBalance
        assert envelope.transaction.operations[0].source.account_id == data["issuer"]
        assert envelope.transaction.operations[0].balance_id == data["claimable_id"]
