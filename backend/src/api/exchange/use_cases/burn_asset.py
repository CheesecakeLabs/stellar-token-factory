from django.utils.translation import gettext_lazy as _

from api.core.helpers.business_errors import (
    DISTRIBUTOR_ACCOUNT_NOT_FOUND,
    INVALID_DISTRIBUTOR_PUBLIC_KEY,
    INVALID_ISSUER_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class BurnAssetUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        distributor: str,
        asset_code: str,
        amount: float,
    ) -> dict:
        """
        Create a burn asset transaction envelope.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            distibutor: Distributor public key (the account must existon the network)
            asset_code: Asset code
            amount: Amount to burn
        """
        # Check if public keys are valid
        self._validate_public_key(issuer, INVALID_ISSUER_PUBLIC_KEY)
        self._validate_public_key(distributor, INVALID_DISTRIBUTOR_PUBLIC_KEY)

        # Check if distributor account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(
            network, distributor, DISTRIBUTOR_ACCOUNT_NOT_FOUND
        )

        # Check if issuer account exists
        self._check_if_account_exists_at_network(
            stellar, issuer, ISSUER_ACCOUNT_NOT_FOUND
        )

        # Payment from distributor to issuer
        transaction_builder = stellar.append_payment_operation(
            destination_public_key=issuer,
            amount=str(amount),
            asset_code=asset_code,
            asset_issuer=issuer,
            source_public_key=distributor,
        )

        required_signatures = set([distributor])

        # Build transaction
        transaction_envelope = stellar.build_transaction(transaction_builder)

        # Converts envelope to XDR
        envelope_xdr = stellar.envelope_to_xdr(transaction_envelope)

        return {
            "envelope_xdr": envelope_xdr,
            "required_signatures": required_signatures,
        }
