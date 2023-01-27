from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_TARGET_PUBLIC_KEY,
    TARGET_ACCOUNT_NOT_FOUND,
    USER_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class CreatePathPaymentStrictReceiveUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        user_id: str,
        destination_public_key: str,
        receive_amount: float,
    ) -> dict:
        """
        Create a path payment strict receive transaction envelope.
        The asset values and send max are mocked based on env vars.
        Params:
            network: Current network (TESTNET or PUBLIC)
            destination_public_key: Destination public key (the account must exist on the network)
            asset_code: Asset code
            receive_amount: Amount of asset that destionation will receive
        """
        # Mocked values
        send_asset = {"code": settings.EUR_CODE, "issuer": settings.EUR_ISSUER}
        receive_asset = {"code": settings.USD_CODE, "issuer": settings.USD_ISSUER}
        send_max = round(settings.SEND_MAX_EUR * receive_amount, 7)

        # Get user signature
        try:
            user_secret, user_threshold = settings.USERS[user_id]
        except KeyError:
            raise BusinessException(
                USER_NOT_FOUND, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if public key is valid
        self._validate_public_key(destination_public_key, INVALID_TARGET_PUBLIC_KEY)

        # Check if source account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(
            network, settings.MAIN_WALLET_PK, ACCOUNT_NOT_FOUND
        )

        # Check if destination account exists
        self._check_if_account_exists_at_network(
            stellar, destination_public_key, TARGET_ACCOUNT_NOT_FOUND
        )

        transaction_builder = stellar.append_path_payment_strict_receive_operation(
            destination_public_key=destination_public_key,
            send_max=send_max,
            dest_amount=receive_amount,
            send_asset_code=send_asset.get("code"),
            send_asset_issuer=send_asset.get("issuer"),
            receive_asset_code=receive_asset.get("code"),
            receive_asset_issuer=receive_asset.get("issuer"),
        )

        # Build transaction
        transaction_envelope = stellar.build_transaction(transaction_builder)

        # Sign transaction
        transaction_envelope = stellar.sign_transaction(
            signatures=[user_secret], envelope=transaction_envelope
        )

        # Converts envelope to XDR
        envelope_xdr = stellar.envelope_to_xdr(transaction_envelope)

        required_signatures = []
        if user_threshold == 1:
            for key, value in settings.USERS.items():
                if key != user_id and value[1] == 1:
                    required_signatures.append(key)
                    break

        return {
            "envelope_xdr": envelope_xdr,
            "final_cost": send_max,
            "required_signatures": required_signatures,
        }
