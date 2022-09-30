import binascii
from typing import Any, Union

from rest_framework import status

from api.core.helpers.business_errors import INVALID_ENVELOPE_XDR, BusinessException
from api.core.use_cases.base_stellar import BaseStellarUseCase


class SubmitEnvelopeUseCase(BaseStellarUseCase):
    def execute(self, network: str, envelope_xdr: str) -> dict[str, Union[bool, Any]]:
        """
        Sends a envelope xdr to the Stellar network.
        Params:
            network: Current network (TESTNET or PUBLIC)
            envelope_xdr: XDR envelope
        """
        # Submit the XDR envelope to the Stellar network
        stellar = self._get_stellar_transaction_class(network)
        try:
            submit_response = stellar.submit_transaction(envelope_xdr)
        except binascii.Error:
            raise BusinessException(
                INVALID_ENVELOPE_XDR, status_code=status.HTTP_400_BAD_REQUEST
            )

        return submit_response
