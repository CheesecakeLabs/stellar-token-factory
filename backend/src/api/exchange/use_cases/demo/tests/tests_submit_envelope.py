from collections import namedtuple

import pytest
from django.conf import settings
from django.test import override_settings
from pytest_mock import MockerFixture
from rest_framework import status
from stellar_sdk.exceptions import BadRequestError

from api.core.helpers.business_errors import BusinessException
from api.exchange.use_cases.demo import SubmitEnvelopeUseCase
from api.exchange.use_cases.tests.mocks import constants
from api.stellar.handlers.error_handler import StellarErrorHandler
from api.stellar.helpers.dtos import Keypair
from api.stellar.helpers.utils import get_network_data

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def test_submit_envelope_fails_when_user_not_found():
    data = {
        "network": "TESTNET",
        "envelope_xdr": constants.ENVELOPE_XDR,
        "user_id": "user-invalid",
        "sign": True,
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 22, 'detail': 'user_not_found'}",
    ):
        SubmitEnvelopeUseCase().execute(**data)


def test_submit_envelope_fails_when_evenelope_is_invalid():
    data = {
        "network": "TESTNET",
        "envelope_xdr": "invalid-envelope",
        "user_id": "user2",
    }
    with pytest.raises(
        BusinessException,
        match="{'code': 7, 'detail': 'invalid_envelope_xdr'}",
    ):
        SubmitEnvelopeUseCase().execute(**data)


def test_submit_envelope_fails_when_network_is_invalid(mocker: MockerFixture):
    data = {"network": "invalid", "envelope_xdr": constants.ENVELOPE_XDR}

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    with pytest.raises(
        BusinessException,
        match="{'code': 19, 'detail': 'invalid_network'}",
    ):
        SubmitEnvelopeUseCase().execute(**data)

    get_network_data_mock.assert_called_with(data.get("network"))


@pytest.mark.parametrize(
    "sign,",
    (True, False),
)
@override_settings(
    USERS={
        "user1": (Keypair().secret, 2),
        "user2": (Keypair().secret, 1),
        "user3": (Keypair().secret, 1),
    }
)
def test_submit_envelope_succesfully(mocker: MockerFixture, sign: bool):
    data = {
        "network": "TESTNET",
        "envelope_xdr": constants.ENVELOPE_XDR,
        "sign": sign,
        "user_id": "user2",
    }

    get_network_data_mock = mocker.patch(
        "api.stellar.helpers.transactions.get_network_data",
        side_effect=get_network_data,
    )

    submit_transaction_mock = mocker.patch(
        "stellar_sdk.Server.submit_transaction",
        return_value=constants.STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY,
    )

    response: dict = SubmitEnvelopeUseCase().execute(**data)

    get_network_data_mock.assert_called_with("TESTNET")
    submit_transaction_mock.assert_called_once()

    assert response == {
        "success": True,
        "message": "Transaction successfully sent to the network.",
        "details": constants.STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY,
    }


def test_submit_envelope_fail_too_late(
    mocker: MockerFixture,
):
    network_passphrase = settings.TEST_NETWORK_PASSPHRASE

    submit_transaction_mock = mocker.patch(
        "stellar_sdk.Server.submit_transaction",
        side_effect=BadRequestError(
            ResponseMock(
                text="BadRequestError",
                status_code=status.HTTP_400_BAD_REQUEST,
                json=lambda: constants.STELLAR_SUBMIT_ENVELOPE_FAIL_TOO_LATE,
            )
        ),
    )

    response: dict = SubmitEnvelopeUseCase().execute(
        network="TESTNET", envelope_xdr=constants.ENVELOPE_XDR
    )

    submit_transaction_mock.assert_called_once()

    assert response == {
        "success": False,
        "message": "Error submitting transaction",
        "details": StellarErrorHandler(
            network_passphrase, constants.STELLAR_SUBMIT_ENVELOPE_FAIL_TOO_LATE
        ).as_dict(),
    }
