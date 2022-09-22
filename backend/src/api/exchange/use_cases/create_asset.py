from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    DISTRIBUTOR_ACCOUNT_NOT_FOUND,
    INVALID_DISTRIBUTOR_PUBLIC_KEY,
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_NETWORK,
    ISSUER_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class CreateAssetUseCase(BaseUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        distributor: str,
        asset_code: str,
        limit: float = None,
    ) -> dict:
        """
        Performs the issuing of an asset.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            distibutor: Distributor public key (the account must exist on the network)
            asset_code: Asset code
            limit: The asset limit that wallet can handle
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

        # Check if distributor account exists and starts the transaction
        try:
            stellar = StellarTransaction(network=network, source_public_key=distributor)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )
        except:
            raise BusinessException(
                DISTRIBUTOR_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Check if issuer account exists
        try:
            stellar.check_if_account_exists_at_network(public_key=issuer)
        except:
            raise BusinessException(
                ISSUER_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Change Trust for distributor
        transaction_builder = stellar.append_change_trust_operation(
            asset_code=asset_code,
            asset_issuer=issuer,
            limit=str(limit) if limit is not None else limit,
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
