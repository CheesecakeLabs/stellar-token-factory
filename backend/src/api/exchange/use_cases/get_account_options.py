from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_NETWORK,
    INVALID_PUBLIC_KEY,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.constants import (
    AUTHORIZATION_CLAWBACK_ENABLED,
    AUTHORIZATION_REVOCABLE,
)
from api.stellar.helpers.exceptions import InvalidNetwork


class GetAccountOptionsUseCase(BaseUseCase):
    def execute(self, network: str, public_key: str) -> dict:
        """
        Get account options
        Params:
        network: Current network (TESTNET or PUBLIC)
            public_key: Account public key
        """

        try:
            stellar = StellarAccount(network=network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            stellar.validate_public_key(public_key=public_key)
        except:
            raise BusinessException(
                INVALID_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = stellar.check_if_account_exists_at_network(public_key=public_key)
        except:
            raise BusinessException(
                ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        account_flags = stellar.get_account_flags(account=account)
        freeze, clawback = False, False
        if AUTHORIZATION_REVOCABLE in account_flags:
            freeze = True
            if AUTHORIZATION_CLAWBACK_ENABLED in account_flags:
                clawback = True

        signers = stellar.get_account_signers(account=account, weight=1)
        if public_key in signers:
            signers.remove(public_key)

        return {"freeze": freeze, "clawback": clawback, "signers": signers}
