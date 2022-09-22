from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk import SignerKeyType
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.set_options import AuthorizationFlag, SetOptions

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import SetOptionsUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_set_options_fails_when_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "public_key": "invalid-key",
        "clawback": True,
        "freeze": True,
        "signers": [],
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 1, 'detail': 'invalid_public_key'}",
    ):
        SetOptionsUseCase().execute(**data)


def test_set_options_fails_when_signer_key_is_invalid():
    data = {
        "network": "TESTNET",
        "public_key": Keypair().public_key,
        "clawback": True,
        "freeze": True,
        "signers": ["invalid"],
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 21, 'detail': 'invalid_signer_key'}",
    ):
        SetOptionsUseCase().execute(**data)


def test_create_asset_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "public_key": Keypair().public_key,
        "clawback": True,
        "freeze": True,
        "signers": [],
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        SetOptionsUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_set_options_fails_when_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "public_key": Keypair().public_key,
        "clawback": True,
        "freeze": True,
        "signers": [],
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
        match="{'code': 2, 'detail': 'account_not_found'}",
    ):
        SetOptionsUseCase().execute(**data)

    load_account_mock.assert_called_with(data["public_key"])


@pytest.mark.parametrize(
    "network,clawback,freeze,signers",
    (
        ("TESTNET", False, False, []),
        ("PUBLIC", True, False, []),
        ("TESTNET", False, True, []),
        ("PUBLIC", False, False, []),
        ("PUBLIC", False, False, None),
        ("TESTNET", True, False, None),
        (
            "TESTNET",
            False,
            False,
            ["GBJ36IYTFDCDZZ6BKSGHI2KELVSA4C7AZ6ZSBA7IFZE3P2RQAIO4H4MX"],
        ),
        (
            "PUBLIC",
            True,
            True,
            ["GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC"],
        ),
        (
            "TESTNET",
            False,
            True,
            [
                "GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC",
                "GBJ36IYTFDCDZZ6BKSGHI2KELVSA4C7AZ6ZSBA7IFZE3P2RQAIO4H4MX",
            ],
        ),
    ),
)
def test_set_options_succesfully(
    mocker: MockerFixture,
    network: str,
    clawback: bool,
    freeze: bool,
    signers: list[str],
):
    data = {
        "network": network,
        "public_key": Keypair().public_key,
        "clawback": clawback,
        "freeze": freeze,
        "signers": signers,
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
                account_id=data["public_key"],
            ),
        ],
    )

    response: dict = SetOptionsUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    acc_get_network_data_mock.assert_called_with(network)
    load_account_mock.assert_called_once()

    assert response.get("required_signatures") == set([data.get("public_key")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    if clawback:
        set_flags = (
            AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED
            | AuthorizationFlag.AUTHORIZATION_REVOCABLE
        )
        clear_flags = None
    elif freeze:
        set_flags = AuthorizationFlag.AUTHORIZATION_REVOCABLE
        clear_flags = AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED
    else:
        set_flags = None
        clear_flags = (
            AuthorizationFlag.AUTHORIZATION_CLAWBACK_ENABLED
            | AuthorizationFlag.AUTHORIZATION_REVOCABLE
        )

    if signers != None:
        current_signer = "GBCCHTXB3HLKHKJFMGF3EABMMHCL3IOMF573AVAXVN2WWJBKZJ7HXFAC"
        if current_signer in signers:
            signer_ops = len(signers) - 1
        else:
            signer_ops = len(signers) + 1
    else:
        signer_ops = 0

    threshold_value = 21 if signers else None

    assert len(envelope.transaction.operations) == 1 + signer_ops
    assert len(envelope.signatures) == 0

    # Set options operation to change flags and thresholds
    assert type(envelope.transaction.operations[0]) == SetOptions
    assert envelope.transaction.operations[0].source.account_id == data["public_key"]
    assert envelope.transaction.operations[0].home_domain == None
    assert envelope.transaction.operations[0].inflation_dest == None
    assert envelope.transaction.operations[0].clear_flags == clear_flags
    assert envelope.transaction.operations[0].set_flags == set_flags
    assert envelope.transaction.operations[0].master_weight == threshold_value
    assert envelope.transaction.operations[0].low_threshold == threshold_value
    assert envelope.transaction.operations[0].med_threshold == threshold_value
    assert envelope.transaction.operations[0].high_threshold == threshold_value
    assert envelope.transaction.operations[0].signer == None

    if signers != None:
        index = 1
        # Set options operations to change signers
        for signer in signers:
            if signer == current_signer:
                continue

            assert type(envelope.transaction.operations[index]) == SetOptions
            assert (
                envelope.transaction.operations[index].source.account_id
                == data["public_key"]
            )
            assert envelope.transaction.operations[index].home_domain == None
            assert envelope.transaction.operations[index].inflation_dest == None
            assert envelope.transaction.operations[index].clear_flags == None
            assert envelope.transaction.operations[index].set_flags == None
            assert envelope.transaction.operations[index].master_weight == None
            assert envelope.transaction.operations[index].low_threshold == None
            assert envelope.transaction.operations[index].med_threshold == None
            assert envelope.transaction.operations[index].high_threshold == None
            assert (
                envelope.transaction.operations[index].signer.signer_key.signer_key_type
                == SignerKeyType.SIGNER_KEY_TYPE_ED25519
            )
            assert (
                envelope.transaction.operations[
                    index
                ].signer.signer_key.encoded_signer_key
                == signer
            )
            assert envelope.transaction.operations[index].signer.weight == 1
            index += 1

        if current_signer not in signers:
            assert type(envelope.transaction.operations[index]) == SetOptions
            assert (
                envelope.transaction.operations[index].source.account_id
                == data["public_key"]
            )
            assert envelope.transaction.operations[index].home_domain == None
            assert envelope.transaction.operations[index].inflation_dest == None
            assert envelope.transaction.operations[index].clear_flags == None
            assert envelope.transaction.operations[index].set_flags == None
            assert envelope.transaction.operations[index].master_weight == None
            assert envelope.transaction.operations[index].low_threshold == None
            assert envelope.transaction.operations[index].med_threshold == None
            assert envelope.transaction.operations[index].high_threshold == None
            assert (
                envelope.transaction.operations[index].signer.signer_key.signer_key_type
                == SignerKeyType.SIGNER_KEY_TYPE_ED25519
            )
            assert (
                envelope.transaction.operations[
                    index
                ].signer.signer_key.encoded_signer_key
                == current_signer
            )
            assert envelope.transaction.operations[index].signer.weight == 0
