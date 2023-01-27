import binascii
from typing import Any, Union

from django.conf import settings
from rest_framework import status

from api.core.helpers.business_errors import (
    INVALID_ENVELOPE_XDR,
    USER_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class SubmitEnvelopeUseCase(BaseStellarUseCase):
    def execute(
        self, network: str, envelope_xdr: str, user_id: str = None, sign: bool = False
    ) -> dict[str, Union[bool, Any]]:
        """
        Sends a envelope xdr to the Stellar network.
        Params:
            network: Current network (TESTNET or PUBLIC)
            envelope_xdr: XDR envelope
            user_id: User ID
            sign: Sign the envelope with the user signature
        """
        # Submit the XDR envelope to the Stellar network
        stellar = self._get_stellar_transaction_class(network)

        if sign:
            try:
                user_secret, _ = settings.USERS[user_id]
            except KeyError:
                raise BusinessException(
                    USER_NOT_FOUND, status_code=status.HTTP_400_BAD_REQUEST
                )
            envelope_xdr = stellar.xdr_to_transaction_envelope(envelope_xdr)
            envelope_xdr = stellar.sign_transaction(
                signatures=[user_secret], envelope=envelope_xdr
            )

        try:
            submit_response = stellar.submit_transaction(envelope_xdr)
        except binascii.Error:
            raise BusinessException(
                INVALID_ENVELOPE_XDR, status_code=status.HTTP_400_BAD_REQUEST
            )

        return submit_response
