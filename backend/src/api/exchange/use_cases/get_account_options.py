from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase
from api.stellar.helpers.constants import (
    AUTHORIZATION_CLAWBACK_ENABLED,
    AUTHORIZATION_REVOCABLE,
)


class GetAccountOptionsUseCase(BaseStellarUseCase):
    def execute(self, network: str, public_key: str) -> dict:
        """
        Get account options
        Params:
        network: Current network (TESTNET or PUBLIC)
            public_key: Account public key
        """

        # Check if public key is valid
        self._validate_public_key(public_key)

        stellar = self._get_stellar_account_class(network)

        account = self._check_if_account_exists_at_network(stellar, public_key)

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
