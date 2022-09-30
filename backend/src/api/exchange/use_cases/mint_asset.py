from django.utils.translation import gettext_lazy as _

from api.core.helpers.business_errors import (
    DISTRIBUTOR_ACCOUNT_NOT_FOUND,
    DISTRIBUTOR_HAS_NO_TRUSTLINE,
    DISTRIBUTOR_HAS_NO_TRUSTLINE_LIMIT,
    INVALID_DISTRIBUTOR_PUBLIC_KEY,
    INVALID_ISSUER_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class MintAssetUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        distributor: str,
        asset_code: str,
        amount: float,
    ) -> dict:
        """
        Create a mint asset transaction envelope.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            distibutor: Distributor public key (the account must exist
            on the network and must have trustline with the asset)
            asset_code: Asset code
            amount: Amount to mint
        """
        # Check if public keys are valid
        self._validate_public_key(issuer, INVALID_ISSUER_PUBLIC_KEY)
        self._validate_public_key(distributor, INVALID_DISTRIBUTOR_PUBLIC_KEY)

        # Check if issuer account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(
            network, issuer, ISSUER_ACCOUNT_NOT_FOUND
        )

        # Check if distributor account exists
        distributor_acc = self._check_if_account_exists_at_network(
            stellar, distributor, DISTRIBUTOR_ACCOUNT_NOT_FOUND
        )

        # Get the distributor asset balance
        stellar_acc = self._get_stellar_account_class(network)
        distributor_balance = stellar_acc.get_acc_balance(
            account=distributor_acc, asset_code=asset_code, asset_issuer=issuer
        )

        # Check if distributor has the asset trustline
        if not distributor_balance:
            raise BusinessException(DISTRIBUTOR_HAS_NO_TRUSTLINE)

        # Check if distributor has the trustline limit to receive this amount
        if float(distributor_balance.get("limit")) < amount:
            raise BusinessException(DISTRIBUTOR_HAS_NO_TRUSTLINE_LIMIT)

        # Payment from issuer to distributor
        transaction_builder = stellar.append_payment_operation(
            destination_public_key=distributor,
            amount=str(amount),
            asset_code=asset_code,
            asset_issuer=issuer,
            source_public_key=issuer,
        )

        required_signatures = set([issuer])

        # Build transaction
        transaction_envelope = stellar.build_transaction(transaction_builder)

        # Converts envelope to XDR
        envelope_xdr = stellar.envelope_to_xdr(transaction_envelope)

        return {
            "envelope_xdr": envelope_xdr,
            "required_signatures": required_signatures,
        }
