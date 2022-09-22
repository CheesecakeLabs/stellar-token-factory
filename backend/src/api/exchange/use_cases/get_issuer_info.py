from typing import List, Union

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


class GetIssuerInfoUseCase(BaseUseCase):
    def execute(
        self,
        network: str,
        public_key: str,
    ) -> dict[str, Union[bool, list]]:
        """
        Get issuer info: assets and clawback and freeze status.
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Wallet public key
        """
        try:
            stellar_acc = StellarAccount(network=network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            stellar_acc.validate_public_key(public_key=public_key)
        except:
            raise BusinessException(
                INVALID_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            account = stellar_acc.check_if_account_exists_at_network(
                public_key=public_key
            )
        except:
            raise BusinessException(
                ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Get issued assets
        assets: List[dict] = stellar_acc.get_assets_by_issuer(public_key=public_key)

        # Get active flags
        account_flags = stellar_acc.get_account_flags(account=account)

        freeze, clawback = False, False
        if AUTHORIZATION_REVOCABLE in account_flags:
            freeze = True
            if AUTHORIZATION_CLAWBACK_ENABLED in account_flags:
                clawback = True

        return {"assets": assets, "clawback": clawback, "freeze": freeze}
