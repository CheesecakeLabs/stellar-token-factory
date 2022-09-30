import copy
from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk import NoneMemo, TextMemo, TrustLineFlags
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.set_trust_line_flags import SetTrustLineFlags

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import UpdateAuthorizedFlagUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_update_auth_flag_fails_when_issuer_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": "invalid-key",
        "target": Keypair().public_key,
        "asset_code": "TKN",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        UpdateAuthorizedFlagUseCase().execute(**data)


def test_update_auth_flag_fails_when_target_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": "invalid-key",
        "asset_code": "TKN",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 10, 'detail': 'invalid_target_public_key'}",
    ):
        UpdateAuthorizedFlagUseCase().execute(**data)


def test_update_auth_flag_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
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
        UpdateAuthorizedFlagUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_update_auth_flag_fails_when_issuer_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
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
    with pytest.raises(
        BusinessException,
        match="{'code': 5, 'detail': 'issuer_account_not_found'}",
    ):
        UpdateAuthorizedFlagUseCase().execute(**data)

    load_account_mock.assert_called_with(data["issuer"])


def test_update_auth_flag_fails_when_target_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
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
    with pytest.raises(
        BusinessException,
        match="{'code': 11, 'detail': 'target_account_not_found'}",
    ):
        UpdateAuthorizedFlagUseCase().execute(**data)

    assert load_account_mock.call_count == 2


def test_update_auth_flag_fails_when_issuer_doesnt_have_auth_revocable_enabled(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
    }
    issuer_account_data = copy.deepcopy(constants.STELLAR_ACCOUNT_RESPONSE)
    issuer_account_data["flags"]["auth_revocable"] = False

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        side_effect=[
            get_mocked_account_object(
                account_id=data["issuer"], data=issuer_account_data
            ),
            get_mocked_account_object(account_id=data["target"]),
        ],
    )
    with pytest.raises(
        BusinessException,
        match="{'code': 16, 'detail': 'issuer_must_have_auth_revocable_flag'}",
    ):
        UpdateAuthorizedFlagUseCase().execute(**data)

    assert load_account_mock.call_count == 2


@pytest.mark.parametrize(
    "network,clear,memo_text",
    (
        ("TESTNET", False, None),
        ("TESTNET", False, "Some text"),
        ("TESTNET", True, None),
        ("TESTNET", True, "Another memo text."),
        ("PUBLIC", False, None),
        ("PUBLIC", False, "Some text"),
        ("PUBLIC", True, None),
        ("PUBLIC", True, "Another memo text."),
    ),
)
def test_update_auth_flag_succesfully(
    mocker: MockerFixture, network: str, clear: bool, memo_text: str
):
    data = {
        "network": network,
        "issuer": Keypair().public_key,
        "target": Keypair().public_key,
        "asset_code": "TKN",
        "clear": clear,
        "memo_text": memo_text,
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

    response: dict = UpdateAuthorizedFlagUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    acc_get_network_data_mock.assert_called_with(network)
    assert load_account_mock.call_count == 2

    assert response.get("required_signatures") == set([data.get("issuer")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    # Set Trustline flags operation
    assert type(envelope.transaction.operations[0]) == SetTrustLineFlags
    assert envelope.transaction.operations[0].source.account_id == data["issuer"]
    assert envelope.transaction.operations[0].trustor == data["target"]
    assert envelope.transaction.operations[0].asset.code == data["asset_code"]
    assert envelope.transaction.operations[0].asset.issuer == data["issuer"]
    assert envelope.transaction.operations[0].clear_flags == (
        TrustLineFlags.AUTHORIZED_FLAG if clear else None
    )
    assert envelope.transaction.operations[0].set_flags == (
        None if clear else TrustLineFlags.AUTHORIZED_FLAG
    )
    if memo_text:
        assert type(envelope.transaction.memo) == TextMemo
        assert envelope.transaction.memo.memo_text.decode("utf-8") == memo_text
    else:
        assert type(envelope.transaction.memo) == NoneMemo
