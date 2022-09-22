from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_NETWORK,
    INVALID_TARGET_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
    ISSUER_MUST_HAVE_AUTH_REVOCABLE_FLAG,
    TARGET_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.constants import AUTHORIZATION_REVOCABLE, AUTHORIZED_FLAG
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction


class UpdateAuthorizedFlagUseCase(BaseUseCase):
    def execute(
        self,
        network: str,
        issuer: str,
        asset_code: str,
        target: str,
        clear: bool = False,
        memo_text: str = None,
    ) -> dict:
        """
        Performs a Set Option op on target trustline.
        Params:
            network: Current network (TESTNET or PUBLIC)
            issuer: Issuer public key (the account must exist on the network)
            asset_code: Asset code
            target: Target public key (the account must exist on the network)
            clear: True to clear the flag, False to set the flag
            memo_text: Memo text to append in the op (optional)
        """
        # Check if issuer public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=issuer)
        except:
            raise BusinessException(
                INVALID_ISSUER_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if target public key is valid
        try:
            StellarTransaction.validate_public_key(public_key=target)
        except:
            raise BusinessException(
                INVALID_TARGET_PUBLIC_KEY, status_code=status.HTTP_404_NOT_FOUND
            )

        # Check if target issuer exists and starts the transaction
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

        # Check if target account exists
        try:
            stellar.check_if_account_exists_at_network(public_key=target)
        except:
            raise BusinessException(
                TARGET_ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        # Check if issuer has the AUTHORIZATION_REVOCABLE flag
        if not StellarAccount(network=network).account_has_flag(
            flag=AUTHORIZATION_REVOCABLE, account=stellar.source_account
        ):
            raise BusinessException(
                ISSUER_MUST_HAVE_AUTH_REVOCABLE_FLAG,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # Set Trustline Flags op default params
        params = {
            "trustor": target,
            "asset_code": asset_code,
            "asset_issuer": issuer,
            "source_public_key": issuer,
        }
        flags = [AUTHORIZED_FLAG]

        # Set Trustline Flags dynamic params
        if clear:
            params.update({"clear_flags": flags})
        else:
            params.update({"set_flags": flags})

        # Set Trustline flags operation
        transaction_builder = stellar.append_set_trustline_flags_operation(**params)

        # Add memo text
        if memo_text:
            transaction_builder = stellar.append_text_memo(
                text=memo_text, transaction_builder=transaction_builder
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
