from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    DISTRIBUTOR_ACCOUNT_NOT_FOUND,
    DISTRIBUTOR_HAS_NO_TRUSTLINE,
    DISTRIBUTOR_HAS_NO_TRUSTLINE_LIMIT,
    INVALID_DISTRIBUTOR_PUBLIC_KEY,
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_NETWORK,
    ISSUER_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class MintAssetUseCase(BaseUseCase):
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
        # Check if issuer public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=issuer)
        except:
            raise BusinessException(
                INVALID_ISSUER_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if distributor public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=distributor)
        except:
            raise BusinessException(
                INVALID_DISTRIBUTOR_PUBLIC_KEY, status_code=status.HTTP_404_NOT_FOUND
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

        # Check if distributor account exists
        try:
            distributor_acc = stellar.check_if_account_exists_at_network(
                public_key=distributor
            )
        except:
            raise BusinessException(
                DISTRIBUTOR_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Get the distributor asset balance
        distributor_balance = StellarAccount(network=network).get_acc_balance(
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
