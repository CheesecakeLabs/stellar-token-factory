from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_NETWORK,
    INVALID_PUBLIC_KEY,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class SetHomeDomainUseCase(BaseUseCase):
    def execute(self, network: str, public_key: str, home_domain: str) -> dict:
        """
        Create a set options transaction envelope to set home domain.
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Account public key (must exist on the network)
            home_domain: Manage Data name
        """
        # Check if public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=public_key)
        except:
            raise BusinessException(
                INVALID_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if account exists and starts the transaction
        try:
            stellar = StellarTransaction(network=network, source_public_key=public_key)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )
        except:
            raise BusinessException(
                ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Append Set options operation
        transaction_builder = stellar.append_set_options_operation(
            home_domain=home_domain,
            source_public_key=public_key,
        )
        required_signatures = set([public_key])

        # Build transaction
        transaction_envelope = stellar.build_transaction(transaction_builder)

        # Converts envelope to XDR
        envelope_xdr = stellar.envelope_to_xdr(transaction_envelope)

        return {
            "envelope_xdr": envelope_xdr,
            "required_signatures": required_signatures,
        }
