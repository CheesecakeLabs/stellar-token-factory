from collections import namedtuple

import pytest
from pytest_mock import MockerFixture

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases import GetAssetDistributorUseCase
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

from .mocks import constants

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_get_asset_distributor_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {
        "network": "invalid",
        "asset_code": "TKN",
        "asset_issuer": Keypair().public_key,
    }

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        GetAssetDistributorUseCase().execute(**data)

    acc_get_network_data_mock.assert_called_with(data.get("network"))


@pytest.mark.parametrize(
    "network,asset_code,asset_issuer,asset_distributor,call_return_value,call_mock_called_times,next_side_effect,next_mock_called_times",
    (
        # Case 0: Find on the first payments page
        (
            "TESTNET",
            "USDC",
            "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
            [constants.STELLAR_GET_PAYMENTS_RESPONSE],
            1,
            [],
            0,
        ),
        (
            "PUBLIC",
            "USDC",
            "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
            [constants.STELLAR_GET_PAYMENTS_RESPONSE],
            1,
            [],
            0,
        ),
        # Case 1: Find on the secord payments page
        (
            "TESTNET",
            "USDC",
            "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
            [constants.STELLAR_GET_PAYMENTS_WITHOUT_PAYMENT_TYPE_RESPONSE],
            1,
            [constants.STELLAR_GET_PAYMENTS_RESPONSE],
            1,
        ),
        (
            "PUBLIC",
            "USDC",
            "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5",
            "GAYF33NNNMI2Z6VNRFXQ64D4E4SF77PM46NW3ZUZEEU5X7FCHAZCMHKU",
            [constants.STELLAR_GET_PAYMENTS_WITHOUT_PAYMENT_TYPE_RESPONSE],
            1,
            [constants.STELLAR_GET_PAYMENTS_RESPONSE],
            1,
        ),
        # Case 3: Not found on payments, found on the first page of accounts
        (
            "TESTNET",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            1,
        ),
        (
            "PUBLIC",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            1,
        ),
        # Case 4: Not found on payments, found on the second page of accounts
        (
            "TESTNET",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
        ),
        (
            "PUBLIC",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            "GBWX6DHQHYIZAH5T4Q2R3JHEPOQ6TJCG3VZ6MWLKQP3XBPIA24TOOV2R",
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
        ),
        # Case 5: Not found on payments or accounts
        (
            "TESTNET",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            None,
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            1,
        ),
        (
            "PUBLIC",
            "TKN",
            "GAP2LI4XUBXNTHAWZBFEAN4IWWMR55KMHWSSEK67I6FSYHMTP3OGV2E6",
            None,
            [
                constants.STELLAR_GET_PAYMENTS_EMPTY_RESPONSE,
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            2,
            [
                constants.STELLAR_GET_ACCOUNTS_EMPTY_RESPONSE,
            ],
            1,
        ),
    ),
)
def test_get_asset_distributor_succesfully(
    mocker: MockerFixture,
    network: str,
    asset_code: str,
    asset_issuer: str,
    asset_distributor: str,
    call_return_value: dict,
    call_mock_called_times: int,
    next_side_effect: list,
    next_mock_called_times: int,
):
    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    call_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.call",
        side_effect=call_return_value,
    )

    next_mock = mocker.patch(
        "stellar_sdk.call_builder.call_builder_sync.base_call_builder.BaseCallBuilder.next",
        side_effect=next_side_effect,
    )

    response: list = GetAssetDistributorUseCase().execute(
        network=network, asset_code=asset_code, asset_issuer=asset_issuer
    )

    acc_get_network_data_mock.assert_called_with(network)

    assert call_mock.call_count == call_mock_called_times
    assert next_mock.call_count == next_mock_called_times

    expected_response = {"public_key": asset_distributor} if asset_distributor else None
    assert response == expected_response
