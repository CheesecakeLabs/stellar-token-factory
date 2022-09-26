from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base_stellar import BaseStellarUseCase


class ManageDataUseCase(BaseStellarUseCase):
    def execute(
        self, network: str, public_key: str, name: str, value: str = None
    ) -> dict:
        """
        Create a manage data transaction envelope.
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Account public key (must exist on the network)
            name: Manage Data name
            value: Data entry value
        """
        # Check if public key is valid
        self._validate_public_key(public_key)

        # Check if account exists and starts the transaction
        stellar = self._get_stellar_transaction_class(network, public_key)

        # Append Manage Data operation
        transaction_builder = stellar.append_manage_data_operation(
            data_name=name,
            data_value=value,
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
