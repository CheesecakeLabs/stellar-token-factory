from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY

INVALID_PUBLIC_KEY = 1
ACCOUNT_NOT_FOUND = 2
INVALID_ISSUER_PUBLIC_KEY = 3
INVALID_DISTRIBUTOR_PUBLIC_KEY = 4
ISSUER_ACCOUNT_NOT_FOUND = 5
DISTRIBUTOR_ACCOUNT_NOT_FOUND = 6
INVALID_ENVELOPE_XDR = 7
DISTRIBUTOR_HAS_NO_TRUSTLINE = 8
DISTRIBUTOR_HAS_NO_TRUSTLINE_LIMIT = 9
INVALID_TARGET_PUBLIC_KEY = 10
TARGET_ACCOUNT_NOT_FOUND = 11
ISSUER_CANNOT_BE_THE_TARGET = 12
NO_TARGET_SELECTED = 13
TARGET_HAS_NO_TRUSTLINE = 14
MISSING_TARGET_FIELDS = 15
ISSUER_MUST_HAVE_AUTH_REVOCABLE_FLAG = 16
INVALID_CLAIMABLE_ID = 17
ISSUER_MUST_HAVE_AUTH_CLAWBACK_FLAG = 18
INVALID_NETWORK = 19
TOML_NOT_FOUND = 20
INVALID_SIGNER_KEY = 21
USER_NOT_FOUND = 22


class BusinessException(APIException, ValidationError):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "unmapped_error"
    default_code = 0

    BUSINESS_ERRORS = {
        INVALID_PUBLIC_KEY: "invalid_public_key",
        ACCOUNT_NOT_FOUND: "account_not_found",
        INVALID_ISSUER_PUBLIC_KEY: "invalid_issuer_public_key",
        INVALID_DISTRIBUTOR_PUBLIC_KEY: "invalid_distributor_public_key",
        ISSUER_ACCOUNT_NOT_FOUND: "issuer_account_not_found",
        DISTRIBUTOR_ACCOUNT_NOT_FOUND: "distributor_account_not_found",
        INVALID_ENVELOPE_XDR: "invalid_envelope_xdr",
        DISTRIBUTOR_HAS_NO_TRUSTLINE: "distributor_has_no_trustline",
        DISTRIBUTOR_HAS_NO_TRUSTLINE_LIMIT: "distributor_has_no_trustline_limit",
        INVALID_TARGET_PUBLIC_KEY: "invalid_target_public_key",
        TARGET_ACCOUNT_NOT_FOUND: "target_account_not_found",
        ISSUER_CANNOT_BE_THE_TARGET: "issuer_cannot_be_the_target",
        NO_TARGET_SELECTED: "no_target_selected",
        TARGET_HAS_NO_TRUSTLINE: "target_has_no_trustline",
        MISSING_TARGET_FIELDS: "missing_target_fields",
        ISSUER_MUST_HAVE_AUTH_REVOCABLE_FLAG: "issuer_must_have_auth_revocable_flag",
        INVALID_CLAIMABLE_ID: "invalid_claimable_id",
        ISSUER_MUST_HAVE_AUTH_CLAWBACK_FLAG: "issuer_must_have_auth_clawback_flag",
        INVALID_NETWORK: "invalid_network",
        TOML_NOT_FOUND: "toml_not_found",
        INVALID_SIGNER_KEY: "invalid_signer_key",
        USER_NOT_FOUND: "user_not_found",
    }

    def __init__(self, error_code: int, status_code: int = None):
        try:
            detail = self.BUSINESS_ERRORS[error_code]
        except KeyError:
            error_code = self.default_code
            detail = self.default_detail

        # Django Rest Framework
        self.detail = {"code": error_code, "detail": detail}

        if status_code:
            self.status_code = status_code

        # Django
        self.message = f"Business error: {detail}"
        self.code = error_code
        self.params = None
        self.error_list = [self]
