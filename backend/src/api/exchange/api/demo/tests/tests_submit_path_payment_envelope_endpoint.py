import json
from collections import namedtuple

import pytest
from django.test.client import Client
from django.urls import reverse
from pytest_mock import MockerFixture
from rest_framework import status
from rest_framework.response import Response
from stellar_sdk.exceptions import BadRequestError

from api.exchange.use_cases.tests.mocks.constants import (
    ENVELOPE_XDR,
    STELLAR_SUBMIT_ENVELOPE_FAIL_TOO_LATE,
    STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY,
)

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")


def post_submit_envelope_request(
    client: Client, network: str = None, **kwargs
) -> Response:
    """
    Make a request to submit an envelope xdr
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:submit-envelope-path-payment"),
        data=json.dumps(kwargs),
        content_type="application/json",
        headers={"network": network},
    )


@pytest.mark.parametrize("network,", ("TESTNET", "PUBLIC"))
def test_submit_envelope_successfully(
    mocker: MockerFixture, client: Client, network: str
) -> None:
    submit_transaction_mock = mocker.patch(
        "stellar_sdk.Server.submit_transaction",
        return_value=STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY,
    )

    response = post_submit_envelope_request(
        client=client, network=network, envelope_xdr=ENVELOPE_XDR, user_id="user1"
    )

    submit_transaction_mock.assert_called_once()

    assert response.status_code == status.HTTP_200_OK

    tx_hash: str = STELLAR_SUBMIT_ENVELOPE_SUCCESSFULLY.get("hash")

    assert response.json() == {
        "transaction_hash": tx_hash,
        "transaction_link": f"https://stellar.expert/explorer/testnet/tx/{tx_hash}",
    }


def test_submit_invalid_envelope(
    client: Client,
) -> None:
    response = post_submit_envelope_request(
        client=client, envelope_xdr="invalid-envelope", user_id="user1"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == {"code": 7, "detail": "invalid_envelope_xdr"}


def test_submit_envelope_with_stellar_error(
    mocker: MockerFixture,
    client: Client,
) -> None:
    submit_transaction_mock = mocker.patch(
        "stellar_sdk.Server.submit_transaction",
        side_effect=BadRequestError(
            ResponseMock(
                text="BadRequestError",
                status_code=status.HTTP_400_BAD_REQUEST,
                json=lambda: STELLAR_SUBMIT_ENVELOPE_FAIL_TOO_LATE,
            )
        ),
    )

    response = post_submit_envelope_request(
        client=client, envelope_xdr=ENVELOPE_XDR, user_id="user1"
    )

    submit_transaction_mock.assert_called_once()

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert response.json() == {
        "stellar_status_code": 400,
        "message": "Err: The ledger closeTime was after the maxTime.",
    }
