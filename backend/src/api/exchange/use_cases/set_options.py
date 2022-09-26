from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.core.helpers.business_errors import INVALID_SIGNER_KEY
from api.core.use_cases.base_stellar import BaseStellarUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.constants import (
    AUTHORIZATION_CLAWBACK_ENABLED,
    AUTHORIZATION_REVOCABLE,
)


class SetOptionsUseCase(BaseStellarUseCase):
    def _get_flags(self, clawback: bool, freeze: bool) -> list[int]:
        if clawback:
            return [AUTHORIZATION_REVOCABLE, AUTHORIZATION_CLAWBACK_ENABLED]
        elif freeze:
            return [AUTHORIZATION_REVOCABLE]
        return []

    def _get_flags_to_remove(self, flags: list[int], acc_flags: list[int]) -> list[int]:
        all_flags = [AUTHORIZATION_REVOCABLE, AUTHORIZATION_CLAWBACK_ENABLED]
        return [f for f in all_flags if (f not in flags and f in acc_flags)]

    def _get_extra_params(self, signers: list) -> dict:
        if signers:
            return {
                "master_weight": settings.DEFAULT_THRESHOLD,
                "low_threshold": settings.DEFAULT_THRESHOLD,
                "med_threshold": settings.DEFAULT_THRESHOLD,
                "high_threshold": settings.DEFAULT_THRESHOLD,
            }
        return {}

    def execute(
        self,
        network: str,
        public_key: str,
        clawback: bool,
        freeze: bool,
        signers: list[str] = None,
    ) -> dict:
        """
        Create a set options transaction envelope to add or remove signers
        and enable or disable Clawback and Freeze flags.
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Account public key (must exist on the network)
            clawback: Set or clear clawback flags (if True freeze is ignored)
            freeze: Set or clear freeze flags
            signers: Updated list of signers with low weight
        """
        # Check if public key is valid
        self._validate_public_key(public_key)

        # Check if signers keys are valid
        for signer in signers or []:
            self._validate_public_key(signer, INVALID_SIGNER_KEY)

        # Check if account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(network, public_key)

        stellar_acc = StellarAccount(network=network)

        # Get flags requested
        flags = self._get_flags(clawback, freeze)

        # Get not selected flags
        account_flags = stellar_acc.get_account_flags(account=stellar.source_account)
        flags_to_remove = self._get_flags_to_remove(flags, account_flags)

        # If there are signers, sets the default threshold values
        extra_params = self._get_extra_params(signers)

        # Append Set options operation to config flags and thresholds
        transaction_builder = stellar.append_set_options_operation(
            set_flags=flags,
            clear_flags=flags_to_remove,
            source_public_key=public_key,
            **extra_params
        )

        if signers != None:
            # Get the list of current signers to check which ones are new and
            # which ones should be deleted
            current_signers = stellar_acc.get_account_signers(
                weight=settings.DEFAULT_SIGNER_LOW_WEIGHT,
                account=stellar.source_account,
            )
            signers_to_remove = [
                s for s in current_signers if (s not in signers) and (s != public_key)
            ]
            signers_to_add = [s for s in signers if s not in current_signers]

            # Add new signers and remove deleted signers
            for signers_data in (
                (signers_to_add, settings.DEFAULT_SIGNER_LOW_WEIGHT),
                (signers_to_remove, 0),
            ):
                for signer in signers_data[0]:
                    transaction_builder = stellar.append_add_account_signer_operation(
                        signer_public_key=signer,
                        weight=signers_data[1],
                        source_public_key=public_key,
                        transaction_builder=transaction_builder,
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
