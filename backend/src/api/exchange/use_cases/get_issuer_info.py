from typing import List, Union

from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase
from api.stellar.helpers.constants import (
    AUTHORIZATION_CLAWBACK_ENABLED,
    AUTHORIZATION_REVOCABLE,
)


class GetIssuerInfoUseCase(BaseStellarUseCase):
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

        # Check if public key is valid
        self._validate_public_key(public_key)

        stellar = self._get_stellar_account_class(network)
        account = self._check_if_account_exists_at_network(stellar, public_key)

        # Get issued assets and assets issued by accounts signed by current account
        assets = []
        accounts_signed: List[dict] = stellar.get_accounts_by_signer(
            public_key=public_key
        )
        for account_signed in accounts_signed:
            assets += stellar.get_assets_by_issuer(
                public_key=account_signed["account_id"]
            )

        # Get active flags
        account_flags = stellar.get_account_flags(account=account)

        freeze, clawback = False, False
        if AUTHORIZATION_REVOCABLE in account_flags:
            freeze = True
            if AUTHORIZATION_CLAWBACK_ENABLED in account_flags:
                clawback = True

        return {"assets": assets, "clawback": clawback, "freeze": freeze}
