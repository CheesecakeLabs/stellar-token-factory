from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    DISTRIBUTOR_ACCOUNT_NOT_FOUND,
    INVALID_DISTRIBUTOR_PUBLIC_KEY,
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_TARGET_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
    ISSUER_CANNOT_BE_THE_TARGET,
    TARGET_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class CreatePaymentUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        distributor: str,
        target: str,
        asset_code: str,
        amount: float,
    ) -> dict:
        """
        Create a payment transaction envelope.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            distibutor: Distributor public key (the account must exist on the network)
            target: Target public key (the account must exist on the network)
            asset_code: Asset code
            amount: Amount of asset to send
        """
        # Check if public keys are valid
        self._validate_public_key(issuer, INVALID_ISSUER_PUBLIC_KEY)
        self._validate_public_key(distributor, INVALID_DISTRIBUTOR_PUBLIC_KEY)
        self._validate_public_key(target, INVALID_TARGET_PUBLIC_KEY)

        # Check if the issuer is not the target
        if issuer == target:
            raise BusinessException(
                ISSUER_CANNOT_BE_THE_TARGET, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if distributor account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(
            network, distributor, DISTRIBUTOR_ACCOUNT_NOT_FOUND
        )

        # Check if issuer account exists
        self._check_if_account_exists_at_network(
            stellar, issuer, ISSUER_ACCOUNT_NOT_FOUND
        )

        # Check if target account exists
        target_acc = self._check_if_account_exists_at_network(
            stellar, target, TARGET_ACCOUNT_NOT_FOUND
        )

        # Get the target asset balance
        target_balance = self._get_stellar_account_class(network).get_acc_balance(
            account=target_acc, asset_code=asset_code, asset_issuer=issuer
        )

        # If target has trustline with the asset, append a Payment op
        if target_balance:
            stellar_op = stellar.append_payment_operation
        # If target has not trustline with the asset, append a Create Claimable Balance op
        else:
            stellar_op = stellar.append_create_claimable_balance_operation

        transaction_builder = stellar_op(
            destination_public_key=target,
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
