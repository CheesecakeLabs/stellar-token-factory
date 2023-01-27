import logging
from functools import reduce
from typing import Any, List, Union

from api.stellar.handlers.error_handler import StellarErrorHandler
from api.stellar.helpers.dtos import Account, Keypair
from api.stellar.helpers.exceptions import AccountNotFoundAtNetwork, InvalidPublicKey
from api.stellar.helpers.utils import get_network_data
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from stellar_sdk import Asset, Claimant, FeeBumpTransaction, FeeBumpTransactionEnvelope
from stellar_sdk import Keypair as StellarKeypair
from stellar_sdk import Server, Signer, TransactionBuilder, TransactionEnvelope
from stellar_sdk.exceptions import (
    BadRequestError,
    Ed25519PublicKeyInvalidError,
    NotFoundError,
)

from .parsers import trustline_flags_parser

logger = logging.getLogger("root")


class StellarTransaction:
    def __init__(self, network: str = "TESTNET", source_public_key: str = None):
        network_data = get_network_data(network)
        self.server = Server(network_data.get("api"))
        self.network_passphrase = network_data.get("passphrase")

        # Stellar team suggested using a fixed value instead of server.fetch_base_fee
        # to avoid errors. However, it is best to check how much we are really
        # willing to spend per transaction, as in recent incidents some users have
        # spent a high amount of lumens doing this.
        self.base_fee = 10000
        self.source_public_key = source_public_key
        self.source_account = (
            self.server.load_account(source_public_key) if source_public_key else None
        )

    def _get_transaction_builder(
        self, transaction_builder: TransactionBuilder = None
    ) -> TransactionBuilder:
        """
        Get or create a default TransactionBuilder.
        """
        return transaction_builder or TransactionBuilder(
            source_account=self.source_account,
            network_passphrase=self.network_passphrase,
            base_fee=self.base_fee,
        )

    def build_transaction(
        self, transaction_builder: TransactionBuilder
    ) -> TransactionEnvelope:
        """
        Build a transaction and returns a TransactionEnvelope.
        """
        return transaction_builder.set_timeout(settings.TRANSACTION_TIMEOUT).build()

    def sign_transaction(
        self,
        signatures: List[str],
        envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
    ) -> Union[TransactionEnvelope, FeeBumpTransactionEnvelope]:
        """
        Signs a transaction envelope (default or fee bump) from a signature list.
        """
        for signature in signatures:
            envelope.sign(signature)
        return envelope

    def submit_transaction(
        self,
        envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
    ) -> dict[str, Union[bool, str, Any]]:
        """
        Submits a transaction to the network.
        """
        transaction_response = dict(
            success=True,
            message=_("Transaction successfully sent to the network."),
            details=None,
        )
        try:
            transaction_response["details"] = self.server.submit_transaction(envelope)
        except BadRequestError as e:
            stellar_error = StellarErrorHandler(self.network_passphrase, e)
            logger.info(msg=stellar_error)
            transaction_response["success"] = False
            transaction_response["message"] = str(_("Error submitting transaction"))
            transaction_response["details"] = stellar_error.as_dict()

        return transaction_response

    def envelope_to_xdr(
        self, envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope]
    ) -> str:
        """
        Converts an envelope (default or fee bump) to XDR format.
        """
        return envelope.to_xdr()

    def xdr_to_transaction_envelope(self, xdr: str) -> TransactionEnvelope:
        """
        Converts a XDR to TransactionEnvelope format.
        """
        return TransactionEnvelope.from_xdr(
            xdr, network_passphrase=self.network_passphrase
        )

    def xdr_to_fee_bump_transaction_envelope(
        self, xdr: str
    ) -> FeeBumpTransactionEnvelope:
        """
        Converts a XDR to FeeBumpTransactionEnvelope format.
        """
        return FeeBumpTransactionEnvelope.from_xdr(
            xdr, network_passphrase=self.network_passphrase
        )

    def build_fee_bump_transaction_envelope(
        self, fee_source: str, transaction_envelope: TransactionEnvelope
    ) -> FeeBumpTransactionEnvelope:
        """
        Creates a FeeBumpTransactionEnvelope object, which represents a fee bump transaction
        envelope ready to sign and submit to send over the network.
        Params:
            fee_source: The account paying for the transaction.
            fee_bump_transaction: The fee bump transaction that is encapsulated in this envelope.
        """
        fee_bump_transaction = FeeBumpTransaction(
            fee_source=fee_source,
            base_fee=self.base_fee,
            inner_transaction_envelope=transaction_envelope,
        )
        return FeeBumpTransactionEnvelope(
            transaction=fee_bump_transaction,
            network_passphrase=self.network_passphrase,
        )

    def append_payment_operation(
        self,
        destination_public_key: str,
        amount: str,
        asset_code: str,
        asset_issuer: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Payment Operation to a transaction, which could be pre-existing or not.
        Params:
            destination_public_key: Account address that receives the payment.
            amount: Amount of asset to send.
            asset_code: Asset code of asset to send to the destination account.
            asset_issuer: Asset issuer of asset to send to the destination account.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended. (OPTIONAL)
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_payment_op(
            destination=destination_public_key,
            asset=Asset(asset_code, asset_issuer),
            amount=amount,
            source=source_public_key or self.source_public_key,
        )

    def append_create_claimable_balance_operation(
        self,
        destination_public_key: str,
        amount: str,
        asset_code: str,
        asset_issuer: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Create Claimbale Balance Operation to a transaction, which could be pre-existing or not.
        Params:
            destination_public_key: Account address that receives the claimable balance.
            amount: Amount of asset to send.
            asset_code: Asset code of asset to send to the destination account.
            asset_issuer: Asset issuer of asset to send to the destination account.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended. (OPTIONAL)
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_create_claimable_balance_op(
            claimants=[Claimant(destination=destination_public_key)],
            asset=Asset(asset_code, asset_issuer),
            amount=amount,
            source=source_public_key or self.source_public_key,
        )

    def append_create_account_operation(
        self,
        destination_public_key: str,
        starting_balance: str = settings.ACCOUNT_STARTING_BALANCE,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Create Account Operation to a transaction, which could be pre-existing
        or not.
        Params:
            destination_public_key: Account address that receives the payment.
            starting_balance: Amount of XLM to send to the newly created account.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_create_account_op(
            destination=destination_public_key,
            starting_balance=starting_balance,
            source=source_public_key or self.source_public_key,
        )

    def append_begin_sponsoring_future_reserves_operation(
        self,
        sponsored_public_key: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Begin Sponsoring Future Reserves Operation to a transaction, which
        could be pre-existing or not.
        Params:
            sponsored_public_key: Account that will have its reserves sponsored.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_begin_sponsoring_future_reserves_op(
            sponsored_id=sponsored_public_key,
            source=source_public_key or self.source_public_key,
        )

    def append_end_sponsoring_future_reserves_operation(
        self,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a End Sponsoring Future Reserves Operation to a transaction, which
        could be pre-existing or not.
        Params:
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_end_sponsoring_future_reserves_op(
            source=source_public_key or self.source_public_key,
        )

    def append_set_options_operation(
        self,
        master_weight: int = None,
        low_threshold: int = None,
        med_threshold: int = None,
        high_threshold: int = None,
        set_flags: List[int] = None,
        clear_flags: List[int] = None,
        home_domain: str = None,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Set Options Operation to a transaction, which could be
        pre-existing or not.
        Params:
            home_domain: Sets the home domain of an account
            master_weight: A number from 0-255 (inclusive) representing the weight of the
                master key. If the weight of the master key is updated to 0, it is
                effectively disabled.
            low_threshold: A number from 0-255 (inclusive) representing the threshold
                this account sets on all operations it performs that have a low threshold.
            med_threshold: A number from 0-255 (inclusive) representing the threshold
                this account sets on all operations it performs that have a medium threshold.
            high_threshold: A number from 0-255 (inclusive) representing the threshold this
                account sets on all operations it performs that have a high threshold.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_set_options_op(
            set_flags=reduce(lambda x, y: x | y, set_flags) if set_flags else None,
            clear_flags=reduce(lambda x, y: x | y, clear_flags)
            if clear_flags
            else None,
            master_weight=master_weight,
            low_threshold=low_threshold,
            med_threshold=med_threshold,
            high_threshold=high_threshold,
            home_domain=home_domain,
            source=source_public_key or self.source_public_key,
        )

    def append_add_account_signer_operation(
        self,
        signer_public_key: str,
        weight: int,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Create a Set Options Operation to add, update, or remove a signer
        from the account, and appends it to a transaction, which could be
        pre-existing or not.
        Params:
            signer_public_key: Signer public key.
            weight: The weight of the signer (0 to delete or 1-255).
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        signer = Signer.ed25519_public_key(account_id=signer_public_key, weight=weight)
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_set_options_op(
            signer=signer,
            source=source_public_key or self.source_public_key,
        )

    def append_change_trust_operation(
        self,
        asset_code: str,
        asset_issuer: str,
        limit: str = None,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Change Trust Operation to a transaction, which
        could be pre-existing or not.
        Params:
            asset_code: Asset code of asset to send to the destination account.
            asset_issuer: Asset issuer of asset to send to the destination account.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_change_trust_op(
            asset=Asset(asset_code, asset_issuer),
            limit=limit,
            source=source_public_key or self.source_public_key,
        )

    def append_set_trustline_flags_operation(
        self,
        trustor: str,
        asset_code: str,
        asset_issuer: str,
        source_public_key: str = None,
        set_flags: List[int] = [],
        clear_flags: List[int] = [],
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Set Trustline Flags operation to a transaction, which
        could be pre-existing or not.
        Params:
            trustor: The account whose trustline this is.
            asset_code: Asset code of asset to send to the destination account.
            asset_issuer: Asset issuer of asset to send to the destination account.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        parsed_set_flags = trustline_flags_parser(set_flags)
        parsed_clear_flags = trustline_flags_parser(clear_flags)

        return transaction_builder.append_set_trust_line_flags_op(
            trustor=trustor,
            asset=Asset(asset_code, asset_issuer),
            source=source_public_key or self.source_public_key,
            set_flags=reduce(lambda x, y: x | y, parsed_set_flags)
            if parsed_set_flags
            else None,
            clear_flags=reduce(lambda x, y: x | y, parsed_clear_flags)
            if parsed_clear_flags
            else None,
        )

    def append_manage_data_operation(
        self,
        data_name: str,
        data_value: str = None,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Manage Data operation to a transaction, which
        could be pre-existing or not.
        Params:
            data_name: If this is a new Name it will add the given name/value pair to the account. If this Name is already present then the associated value will be modified.
            data_value: If not present then the existing data_name will be deleted. If present then this value will be set in the DataEntry.
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended (OPTIONAL).
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_manage_data_op(
            data_name=data_name,
            data_value=data_value,
            source=source_public_key or self.source_public_key,
        )

    def append_clawback_operation(
        self,
        amount: str,
        asset_code: str,
        asset_issuer: str,
        from_public_key: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Clawback Operation to a transaction, which
        could be pre-existing or not.
        Params:
            amount: Amount to clawback.
            asset_code: Asset code of asset.
            asset_issuer: Asset issuer.
            from_public_key: The account to clawback from.
            source_public_key: The source account for the operation. Defaults to the transaction's source account. (OPTIONAL)
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_clawback_op(
            asset=Asset(asset_code, asset_issuer),
            from_=from_public_key,
            amount=amount,
            source=source_public_key or self.source_public_key,
        )

    def append_clawback_claimable_balance_operation(
        self,
        claimable_id: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Clawback Operation to a transaction, which
        could be pre-existing or not.
        Params:
            claimable_id: The claimable balance ID to be clawed back.
            source_public_key: The source account for the operation. Defaults to the transaction's source account. (OPTIONAL)
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_clawback_claimable_balance_op(
            balance_id=claimable_id,
            source=source_public_key or self.source_public_key,
        )

    def append_text_memo(
        self,
        text: str,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a memo text to a transaction, which
        could be pre-existing or not.
        Params:
            text: The text for the memo to add.
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.add_text_memo(
            memo_text=text,
        )

    def append_path_payment_strict_receive_operation(
        self,
        destination_public_key: str,
        send_max: float,
        dest_amount: float,
        send_asset_code: str,
        send_asset_issuer: str,
        receive_asset_code: str,
        receive_asset_issuer: str,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Path Payment Strict Receive to a transaction
        Params:
            source_public_key: Public Key from the source.
            destination_public_key: Public Key from the destination.
            dest_amount: Amount of asset to that destination will receive.
            send_max: Max amount of asset to send.
            send_asset_code: Asset code of asset to send.
            send_asset_issuer: Issuer public key (send asset)
            receive_asset_issuer:  Issuer public key (receive asset)
            receive_asset_code: Asset code of asset to receive.
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_path_payment_strict_receive_op(
            destination=destination_public_key,
            source=source_public_key or self.source_public_key,
            send_asset=Asset(send_asset_code, send_asset_issuer),
            dest_asset=Asset(receive_asset_code, receive_asset_issuer),
            dest_amount=str(dest_amount),
            send_max=str(send_max),
            path=[],
        )

    def append_manage_sell_offer(
        self,
        amount: str,
        sell_asset_code: str,
        sell_issuer_public_key: str,
        buy_issuer_public_key: str,
        buy_asset_code: str,
        price: float,
        offer_id: int,
        source_public_key: str = None,
        transaction_builder: TransactionBuilder = None,
    ) -> TransactionBuilder:
        """
        Appends a Sell Offer to a transaction, which could be pre-existing or not.
        Params:
            amount: Amount of asset to send.
            sell_asset_code: Asset code of asset to sell.
            sell_issuer_public_key: Issuer public key (sell asset)
            buy_issuer_public_key:  Issuer public key (buy asset)
            buy_asset_code: Asset code of asset to buy.
            price: The asset price to buy
            offer_id: Id of this offer (optional)
            source_public_key: Source account, the default is defined in the class. (OPTIONAL)
            transaction_builder: Existing TransactionBuilder for the operation to be
                appended. (OPTIONAL)
        """
        transaction_builder = self._get_transaction_builder(transaction_builder)
        return transaction_builder.append_manage_sell_offer_op(
            selling=Asset(sell_asset_code, sell_issuer_public_key),
            buying=Asset(buy_asset_code, buy_issuer_public_key),
            amount=str(amount),
            price=str(price),
            offer_id=offer_id,
            source=source_public_key or self.source_public_key,
        )

    def generate_keypair(self) -> Keypair:
        """
        Return a randomly generated keypair.
        """
        keypair = StellarKeypair.random()
        return Keypair(public_key=keypair.public_key, secret=keypair.secret)

    @classmethod
    def validate_public_key(cls, public_key: str) -> Keypair:
        try:
            keypair = StellarKeypair.from_public_key(public_key)
        except Ed25519PublicKeyInvalidError:
            raise InvalidPublicKey(
                f"Invalid Public Key provided. Public Key: {public_key}"
            )
        else:
            return Keypair(public_key=keypair.public_key)

    def check_if_account_exists_at_network(self, public_key: str) -> Account:
        try:
            return self.server.load_account(public_key)
        except NotFoundError as e:
            logger.info(msg=StellarErrorHandler(self.network_passphrase, e).as_json())
            raise AccountNotFoundAtNetwork(
                f"Account not found at network. Public Key: {public_key}"
            )
