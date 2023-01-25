from django.test import override_settings
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response

from api.exchange.use_cases.demo.tests.mocks import constants
from api.exchange.use_cases.tests.mocks.utils import get_mocked_account_object
from api.stellar.helpers.utils import get_network_data


def get_main_wallet_eur_balance_request(
    client: Client,
) -> Response:
    """
    Make a request to get main wallet EUR balance
    Args:
        client: HTTP Client
    """
    return client.get(
        path=reverse(
            "exchange:get-main-wallet-eur-balance",
        ),
        content_type="application/json",
    )


@override_settings(
    MAIN_WALLET_PK="GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ",
    EUR_CODE="EUR",
    EUR_ISSUER="GC3XSOYSQDYBBGBBMV7OBZJOZQL47POSV6R4WPPXQVYMIEQBDFTAK46U",
)
def test_get_main_wallet_eur_balance_successfully(
    mocker: MockerFixture,
    client: Client,
) -> None:

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(data=constants.STELLAR_ACCOUNT_RESPONSE),
    )

    response = get_main_wallet_eur_balance_request(client=client)

    load_account_mock.assert_called_once()
    acc_get_network_data_mock.assert_called_once()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "balance": 10000000000.0,
        "asset_code": "EUR",
        "asset_issuer": "GC3XSOYSQDYBBGBBMV7OBZJOZQL47POSV6R4WPPXQVYMIEQBDFTAK46U",
    }


@override_settings(
    MAIN_WALLET_PK="GDIRWLYTROHTR42SZ2KYU4D6S2DGZIPALUWA4RBQIJLQZT3TLV7ADUTJ",
    EUR_CODE="USD",
    EUR_ISSUER="GC3XSOYSQDYBBGBBMV7OBZJOZQL47POSV6R4WPPXQVYMIEQBDFTAK46U",
)
def test_get_main_wallet_eur_balance_not_found(
    mocker: MockerFixture,
    client: Client,
) -> None:

    acc_get_network_data_mock = mocker.patch(
        "api.stellar.helpers.accounts.get_network_data",
        side_effect=get_network_data,
    )

    load_account_mock = mocker.patch(
        "stellar_sdk.Server.load_account",
        return_value=get_mocked_account_object(data=constants.STELLAR_ACCOUNT_RESPONSE),
    )

    response = get_main_wallet_eur_balance_request(client=client)

    load_account_mock.assert_called_once()
    acc_get_network_data_mock.assert_called_once()

    assert response.status_code == status.HTTP_404_NOT_FOUND
