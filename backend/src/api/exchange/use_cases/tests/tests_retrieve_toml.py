import copy
from collections import namedtuple

import pytest
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import NotFoundError

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import RetrieveTOMLUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

from .mocks import constants
from .mocks.utils import get_mocked_account_object

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_retrieve_toml_fails_when_public_key_is_invalid():
    data = {
        "network": "TESTNET",
        "public_key": "invalid-key",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 3, 'detail': 'invalid_issuer_public_key'}",
    ):
        RetrieveTOMLUseCase().execute(**data)


def test_retrieve_toml_fails_when_network_is_invalid():
    data = {"network": "invalid", "public_key": Keypair().public_key}
    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        RetrieveTOMLUseCase().execute(**data)


def test_retrieve_toml_fails_when_account_not_found(
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
        RetrieveTOMLUseCase().execute(**data)

    load_account_mock.assert_called_with(data.get("public_key"))


def test_retrieve_toml_fails_when_toml_not_found(
    mocker: MockerFixture,
):
    data = {"network": "TESTNET", "public_key": Keypair().public_key}

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=data.get("public_key")),
    )

    fetch_stellar_toml_mock = mocker.patch(
        "stellar_sdk.sep.stellar_toml.fetch_stellar_toml",
        side_effect=ConnectionError(),
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 20, 'detail': 'toml_not_found'}",
    ):
        RetrieveTOMLUseCase().execute(**data)

    load_account_mock.assert_called_with(data.get("public_key"))
    fetch_stellar_toml_mock.assert_called_once()


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_retrieve_toml_succesfully(
    mocker: MockerFixture,
    network: str,
):
    public_key: str = Keypair().public_key

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(account_id=public_key),
    )

    fetch_stellar_toml_mock = mocker.patch(
        "stellar_sdk.sep.stellar_toml.fetch_stellar_toml",
        return_value=copy.deepcopy(constants.FETCH_STELLAR_TOML_RESPONSE),
    )

    response: dict = RetrieveTOMLUseCase().execute(
        network=network, public_key=public_key
    )

    acc_get_network_data_mock.assert_called_with(network)
    load_account_mock.assert_called_once()
    fetch_stellar_toml_mock.assert_called_with(domain=None)

    assert response == constants.RETRIEVE_TOML_RESPONSE
