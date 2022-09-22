from os import stat

from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    INVALID_CLAIMABLE_ID,
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_NETWORK,
    INVALID_TARGET_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
    ISSUER_CANNOT_BE_THE_TARGET,
    ISSUER_MUST_HAVE_AUTH_CLAWBACK_FLAG,
    MISSING_TARGET_FIELDS,
    NO_TARGET_SELECTED,
    TARGET_ACCOUNT_NOT_FOUND,
    TARGET_HAS_NO_TRUSTLINE,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.constants import AUTHORIZATION_CLAWBACK_ENABLED
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class CreateClawbackUseCase(BaseUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        asset_code: str = None,
        amount: float = None,
        target: str = None,
        claimable_id: str = None,
    ) -> dict:
        """
        Create a Clawback transaction envelope.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            asset_code: Asset code
            amount: Amount of asset to clawback
            target: Target public key (the account must exist on the network)
            claimable_id: Claimable ID
        """
        if not target and not claimable_id:
            raise BusinessException(
                NO_TARGET_SELECTED, status_code=status.HTTP_400_BAD_REQUEST
            )

        if target and not (asset_code and amount):
            raise BusinessException(
                MISSING_TARGET_FIELDS, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if issuer public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=issuer)
        except:
            raise BusinessException(
                INVALID_ISSUER_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if issuer account exists and starts the transaction
        try:
            stellar = StellarTransaction(network=network, source_public_key=issuer)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )
        except:
            raise BusinessException(
                ISSUER_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        stellar_acc = StellarAccount(network=network)
        # Check if issuer has the AUTHORIZATION_CLAWBACK_ENABLED flag
        if not stellar_acc.account_has_flag(
            flag=AUTHORIZATION_CLAWBACK_ENABLED, account=stellar.source_account
        ):
            raise BusinessException(
                ISSUER_MUST_HAVE_AUTH_CLAWBACK_FLAG,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if target:
            # Check if target public key is valid
            try:
                StellarTransaction.validate_public_key(public_key=target)
            except:
                raise BusinessException(
                    INVALID_TARGET_PUBLIC_KEY,
                    status_code=status.HTTP_404_NOT_FOUND,
                )

            # Check if the issuer is not the target
            if issuer == target:
                raise BusinessException(
                    ISSUER_CANNOT_BE_THE_TARGET, status_code=status.HTTP_400_BAD_REQUEST
                )

            # Check if target account exists
            try:
                target_acc = stellar.check_if_account_exists_at_network(
                    public_key=target
                )
            except:
                raise BusinessException(
                    TARGET_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
                )

            # Get the target asset balance
            target_balance = stellar_acc.get_acc_balance(
                account=target_acc, asset_code=asset_code, asset_issuer=issuer
            )

            # If target has trustline with the asset
            if not target_balance:
                raise BusinessException(TARGET_HAS_NO_TRUSTLINE)

            transaction_builder = stellar.append_clawback_operation(
                from_public_key=target,
                amount=str(amount),
                asset_code=asset_code,
                asset_issuer=issuer,
                source_public_key=issuer,
            )
        else:
            try:
                transaction_builder = (
                    stellar.append_clawback_claimable_balance_operation(
                        claimable_id=claimable_id,
                        source_public_key=issuer,
                    )
                )
            except ValueError:
                raise BusinessException(
                    INVALID_CLAIMABLE_ID, status_code=status.HTTP_400_BAD_REQUEST
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
