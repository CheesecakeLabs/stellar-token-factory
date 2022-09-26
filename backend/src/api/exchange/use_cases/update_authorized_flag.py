from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_TARGET_PUBLIC_KEY,
    ISSUER_ACCOUNT_NOT_FOUND,
    ISSUER_MUST_HAVE_AUTH_REVOCABLE_FLAG,
    TARGET_ACCOUNT_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base_stellar import BaseStellarUseCase
from api.stellar.helpers.constants import AUTHORIZATION_REVOCABLE, AUTHORIZED_FLAG


class UpdateAuthorizedFlagUseCase(BaseStellarUseCase):
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
        # Check if public keys are valid
        self._validate_public_key(issuer, INVALID_ISSUER_PUBLIC_KEY)
        self._validate_public_key(target, INVALID_TARGET_PUBLIC_KEY)

        # Check if target issuer exists and starts the transaction
        stellar = self._get_stellar_transaction_class(
            network, issuer, ISSUER_ACCOUNT_NOT_FOUND
        )

        # Check if target account exists
        self._check_if_account_exists_at_network(
            stellar, target, TARGET_ACCOUNT_NOT_FOUND
        )

        # Check if issuer has the AUTHORIZATION_REVOCABLE flag
        stellar_acc = self._get_stellar_account_class(network)
        if not stellar_acc.account_has_flag(
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
