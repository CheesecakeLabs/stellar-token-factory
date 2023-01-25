from typing import List

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase


class GetMainWalletBalance(BaseStellarUseCase):
    def execute(self, network: str, asset_code: str, asset_issuer: str) -> dict:
        """
        Get main wallet EUR balance.
        Params:
            network: Current network (TESTNET or PUBLIC)
            asset_code: Asset code
            asset_issuer: Asset issuer
        """
        self._validate_public_key(settings.MAIN_WALLET_PK)

        stellar = self._get_stellar_account_class(network)
        account = self._check_if_account_exists_at_network(
            stellar, settings.MAIN_WALLET_PK
        )
        return stellar.get_acc_balance(
            account=account, asset_code=asset_code, asset_issuer=asset_issuer
        )
