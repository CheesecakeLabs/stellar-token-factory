from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import INVALID_NETWORK, BusinessException
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.exceptions import InvalidNetwork


class GetAssetDistributorUseCase(BaseUseCase):
    def execute(self, network: str, asset_code: str, asset_issuer: str) -> dict:
        """
        Get asset distributor's public key.
        Params:
        network: Current network (TESTNET or PUBLIC)
            asset_code: Asset code
            asset_issuer: Asset issuer
        """

        try:
            stellar = StellarAccount(network=network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

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
