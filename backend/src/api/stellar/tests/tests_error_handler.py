import json
from collections import namedtuple

from django.conf import settings
from rest_framework import status
from stellar_sdk.exceptions import BadRequestError

from api.stellar.handlers.error_handler import StellarErrorHandler
from api.stellar.tests.mocks.constants import (
    MISSING_ONE_SIGNATURE,
    NO_SHAPE_TRANSACTION,
    WRONG_ACCOUNT_FORMAT,
)

ResponseMock = namedtuple("ResponseMock", "text,status_code,json")

missing_one_signature = StellarErrorHandler(
    settings.TEST_NETWORK_PASSPHRASE, MISSING_ONE_SIGNATURE
)
no_shape_transaction = StellarErrorHandler(
    settings.TEST_NETWORK_PASSPHRASE, NO_SHAPE_TRANSACTION
)
wrong_account_format = StellarErrorHandler(
    settings.TEST_NETWORK_PASSPHRASE, WRONG_ACCOUNT_FORMAT
)


def test_error_handler_data_types() -> None:
    assert isinstance(missing_one_signature.get_title(), str)
    assert isinstance(missing_one_signature.get_message(), str)
    assert isinstance(missing_one_signature.get_status(), int)
    assert isinstance(missing_one_signature.get_tx_codes(), str)
    assert isinstance(missing_one_signature.get_operations(), list)
    assert isinstance(missing_one_signature.get_more_details(), str)
    assert isinstance(missing_one_signature.get_stellar_error(), dict)

    assert type(str(no_shape_transaction.has_any_info())) is str
    assert type(missing_one_signature.as_json()) is str
    assert type(json.loads(missing_one_signature.as_json())) is dict
    assert type(missing_one_signature.as_dict()) is dict


def test_error_handler_data_values() -> None:
    assert no_shape_transaction.has_any_info() is False
    assert missing_one_signature.has_any_info() is True
    assert missing_one_signature.get_title() == "Transaction Failed"
    assert missing_one_signature.get_message() == "Err: One of the operations failed."
    assert missing_one_signature.get_status() == 400
    assert missing_one_signature.get_tx_codes() == "tx_failed"
    assert missing_one_signature.get_operations() == [
        {
            "code": "op_success",
            "detail": "BEGIN_SPONSORING_FUTURE_RESERVES",
            "index": 0,
        },
        {"code": "op_success", "detail": "CREATE_ACCOUNT", "index": 1},
        {
            "code": "op_bad_auth",
            "detail": "Err: needs more signatures to complete this operation.",
            "index": 2,
        },
    ]
    assert (
        missing_one_signature.get_more_details()
        == "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/"
    )
    assert missing_one_signature.get_stellar_error() == MISSING_ONE_SIGNATURE
    assert wrong_account_format.has_any_info() is True
    assert wrong_account_format.get_message() is None
    assert wrong_account_format.get_status() == 400
    assert wrong_account_format.get_tx_codes() is None
    assert wrong_account_format.get_operations() == [
        {
            "invalid_field": "account_id",
            "reason": "Account ID must start with `G` and contain 56 alphanum "
            "characters",
        }
    ]
    assert (
        wrong_account_format.get_more_details()
        == "The request you sent was invalid in some way."
    )
    assert wrong_account_format.get_stellar_error() == WRONG_ACCOUNT_FORMAT


def test_error_handler_when_base_horizon_error_object_is_provided():
    bad_request_error = BadRequestError(
        ResponseMock(
            text="BadRequestError",
            status_code=status.HTTP_400_BAD_REQUEST,
            json=lambda: MISSING_ONE_SIGNATURE,
        )
    )

    error_handler = StellarErrorHandler(
        settings.TEST_NETWORK_PASSPHRASE, bad_request_error
    )

    assert error_handler.get_status() == status.HTTP_400_BAD_REQUEST
    assert error_handler.get_title() == "Transaction Failed"
    assert error_handler.get_message() == "Err: One of the operations failed."
    assert error_handler.has_any_info() is True
    assert error_handler.get_stellar_error() == MISSING_ONE_SIGNATURE
    assert error_handler.get_tx_codes() == "tx_failed"
    assert error_handler.get_operations() == [
        {
            "code": "op_success",
            "detail": "BEGIN_SPONSORING_FUTURE_RESERVES",
            "index": 0,
        },
        {"code": "op_success", "detail": "CREATE_ACCOUNT", "index": 1},
        {
            "code": "op_bad_auth",
            "detail": "Err: needs more signatures to complete this operation.",
            "index": 2,
        },
    ]
    assert (
        error_handler.get_more_details()
        == "The transaction failed when submitted to the stellar network. The `extras.result_codes` field on this response contains further details.  Descriptions of each code can be found at: https://developers.stellar.org/api/errors/http-status-codes/horizon-specific/transaction-failed/"
    )
