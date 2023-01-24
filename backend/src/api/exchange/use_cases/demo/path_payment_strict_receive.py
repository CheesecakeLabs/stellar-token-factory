from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_TARGET_PUBLIC_KEY,
    TARGET_ACCOUNT_NOT_FOUND,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase


class CreatePathPaymentStrictReceiveUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        destination_public_key: str,
        receive_amount: float,
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
        # Mocked values
        send_asset = {"code": settings.EUR_CODE, "issuer": settings.EUR_ISSUER}
        receive_asset = {"code": settings.USD_CODE, "issuer": settings.USD_ISSUER}
        send_max = settings.SEND_MAX_EUR * receive_amount

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
            signatures=[settings.MAIN_WALLET_SK], envelope=transaction_envelope
        )

        # Converts envelope to XDR
        envelope_xdr = stellar.envelope_to_xdr(transaction_envelope)

        return {
            "envelope_xdr": envelope_xdr,
        }
