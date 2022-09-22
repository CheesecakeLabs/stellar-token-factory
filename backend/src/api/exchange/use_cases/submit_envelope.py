import binascii
from typing import Any, Union

from rest_framework import status

from api.core.helpers.business_errors import (
    INVALID_ENVELOPE_XDR,
    INVALID_NETWORK,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class SubmitEnvelopeUseCase(BaseUseCase):
    def execute(self, network: str, envelope_xdr: str) -> dict[str, Union[bool, Any]]:
        """
        Sends a envelope xdr to the Stellar network.
        Params:
            network: Current network (TESTNET or PUBLIC)
            envelope_xdr: XDR envelope
        """
        # Submit the XDR envelope to the Stellar network
        try:
            submit_response = StellarTransaction(network=network).submit_transaction(
                envelope_xdr
            )
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )
        except binascii.Error:
            raise BusinessException(
                INVALID_ENVELOPE_XDR, status_code=status.HTTP_400_BAD_REQUEST
            )

        return submit_response
