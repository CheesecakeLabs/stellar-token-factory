from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase


class SetHomeDomainUseCase(BaseStellarUseCase):
    def execute(self, network: str, public_key: str, home_domain: str) -> dict:
        """
        Create a set options transaction envelope to set home domain.
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Account public key (must exist on the network)
            home_domain: Manage Data name
        """
        # Check if public key is valid
        self._validate_public_key(public_key)

        # Check if account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(network, public_key)

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
