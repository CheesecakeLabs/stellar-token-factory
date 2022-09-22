from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.operation.set_options import SetOptions

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import SetHomeDomainUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.transactions import StellarTransaction
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_set_home_domain_fails_when_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "public_key": "invalid-key",
        "home_domain": "domain.com",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 1, 'detail': 'invalid_public_key'}",
    ):
        SetHomeDomainUseCase().execute(**data)


def test_create_asset_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "public_key": Keypair().public_key,
        "home_domain": "domain.com",
    }
    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        SetHomeDomainUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


def test_set_home_domain_fails_when_account_not_found(
    mocker: MockerFixture,
):
    data = {
        "network": "TESTNET",
        "public_key": Keypair().public_key,
        "home_domain": "domain.com",
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
        SetHomeDomainUseCase().execute(**data)

    load_account_mock.assert_called_with(data["public_key"])


@pytest.mark.parametrize(
    "network,",
    ("TESTNET", "PUBLIC"),
)
def test_set_home_domain_succesfully(mocker: MockerFixture, network: str):
    data = {
        "network": network,
        "public_key": Keypair().public_key,
        "home_domain": "domain.com",
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
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

    response: dict = SetHomeDomainUseCase().execute(**data)

    get_network_data_mock.assert_called_with(network)
    load_account_mock.assert_called_once()

    assert response.get("required_signatures") == set([data.get("public_key")])

    envelope = StellarTransaction().xdr_to_transaction_envelope(
        response["envelope_xdr"]
    )

    assert len(envelope.transaction.operations) == 1
    assert len(envelope.signatures) == 0

    # Set options operation
    assert type(envelope.transaction.operations[0]) == SetOptions
    assert envelope.transaction.operations[0].source.account_id == data["public_key"]
    assert envelope.transaction.operations[0].home_domain == data["home_domain"]
    assert envelope.transaction.operations[0].inflation_dest == None
    assert envelope.transaction.operations[0].clear_flags == None
    assert envelope.transaction.operations[0].set_flags == None
    assert envelope.transaction.operations[0].master_weight == None
    assert envelope.transaction.operations[0].low_threshold == None
    assert envelope.transaction.operations[0].med_threshold == None
    assert envelope.transaction.operations[0].high_threshold == None
    assert envelope.transaction.operations[0].signer == None
