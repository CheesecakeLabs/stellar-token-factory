from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase


class GetAssetDistributorUseCase(BaseStellarUseCase):
    def execute(self, network: str, asset_code: str, asset_issuer: str) -> dict:
        """
        Get asset distributor's public key.
        Params:
            network: Current network (TESTNET or PUBLIC)
            asset_code: Asset code
            asset_issuer: Asset issuer
        """

        stellar = self._get_stellar_account_class(network)

        # Try to find distributor by issuer payments
        first_payment = stellar.get_first_payment_of_an_account(
            public_key=asset_issuer, asset_code=asset_code, asset_issuer=asset_issuer
        )
        if first_payment:
            return {"public_key": first_payment.get("to")}

        # Try to find distributor by the asset trustlines
        last_modified_trustline = stellar.get_account_with_last_modified_trustline(
            asset_code=asset_code, asset_issuer=asset_issuer
        )
        if last_modified_trustline:
            return {"public_key": last_modified_trustline.get("account_id")}

        return None
