import logging
from typing import Dict, List, Union

from django.utils.translation import gettext_lazy as _
from stellar_sdk import Asset
from stellar_sdk import Keypair as StellarKeypair
from stellar_sdk import Server
from stellar_sdk.exceptions import Ed25519PublicKeyInvalidError, NotFoundError
from stellar_sdk.sep import stellar_toml

from api.stellar.handlers.error_handler import StellarErrorHandler
from api.stellar.helpers import constants
from api.stellar.helpers.dtos import Account, Keypair
from api.stellar.helpers.exceptions import AccountNotFoundAtNetwork, InvalidPublicKey

from .utils import get_network_data

logger = logging.getLogger("root")


class StellarAccount:
    def __init__(self, network: str = "TESTNET"):
        network_data = get_network_data(network)
        self.server = Server(network_data.get("api"))
        self.network_passphrase = network_data.get("passphrase")

    def load_account(self, public_key: str) -> dict:
        """
        Loads the account from the server.
        Params:
            public_key: The wallet Public Key.
        """
        return self.server.load_account(public_key).raw_data

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

    def get_assets_by_issuer(self, public_key: str) -> list:
        assets_records = []
        assets_call_builder = self.server.assets().for_issuer(public_key).limit(100)
        assets_records += assets_call_builder.call()["_embedded"]["records"]

        while page_records := assets_call_builder.next()["_embedded"]["records"]:
            assets_records += page_records

        return assets_records

    def get_first_payment_of_an_account(
        self, public_key: str, asset_code: str = None, asset_issuer: str = None
    ) -> dict:
        get_by_asset = True if (asset_code and asset_issuer) else False
        payments_records = []

        payments_call_builder = (
            self.server.payments().for_account(public_key).order(desc=False).limit(10)
        )
        payments_records += payments_call_builder.call()["_embedded"]["records"]

        while payments_records:
            for payment in payments_records:
                if payment.get("type") == "payment":
                    if get_by_asset:
                        if (
                            payment.get("asset_code") == asset_code
                            and payment.get("asset_issuer") == asset_issuer
                        ):
                            return payment
                    else:
                        return payment
            payments_records = payments_call_builder.next()["_embedded"]["records"]

    def get_account_with_last_modified_trustline(
        self, asset_code: str, asset_issuer: str
    ) -> dict:
        accounts_call_builder = (
            self.server.accounts().for_asset(Asset(asset_code, asset_issuer)).limit(50)
        )
        accounts_records = []

        # Get all asset accounts first
        accounts_records += accounts_call_builder.call()["_embedded"]["records"]
        while page_records := accounts_call_builder.next()["_embedded"]["records"]:
            accounts_records += page_records

        if not accounts_records:
            return None

        # Starts the older block with infinite value
        older_block = (None, float("inf"))
        for account in accounts_records:
            for balance in account.get("balances", []):
                if (
                    balance.get("asset_code") == asset_code
                    and balance.get("asset_issuer") == asset_issuer
                ):
                    # If the block is older than the oldest block so far
                    if balance.get("last_modified_ledger") < older_block[1]:
                        older_block = (account, balance.get("last_modified_ledger"))

        return older_block[0]

    def get_acc_balance(
        self,
        asset_code: str,
        asset_issuer: str,
        public_key: str = None,
        account: Account = None,
    ) -> Dict[str, Union[str, int]]:
        if not account:
            account = self.check_if_account_exists_at_network(public_key=public_key)

        balances: List[dict] = account.raw_data.get("balances")
        balance_obj = next(
            (
                x
                for x in balances
                if (
                    x.get("asset_code") == asset_code
                    and x.get("asset_issuer") == asset_issuer
                )
            ),
            None,
        )
        return balance_obj

    def account_has_flag(
        self,
        flag: int,
        public_key: str = None,
        account: Account = None,
    ) -> bool:
        if not account:
            account = self.check_if_account_exists_at_network(public_key=public_key)

        flags_dict = {
            constants.AUTHORIZATION_REQUIRED: "auth_required",
            constants.AUTHORIZATION_REVOCABLE: "auth_revocable",
            constants.AUTHORIZATION_IMMUTABLE: "auth_immutable",
            constants.AUTHORIZATION_CLAWBACK_ENABLED: "auth_clawback_enabled",
        }

        return account.raw_data["flags"].get(flags_dict[flag])

    def get_account_flags(
        self,
        public_key: str = None,
        account: Account = None,
    ) -> list[int]:
        if not account:
            account = self.check_if_account_exists_at_network(public_key=public_key)

        flags_dict = {
            "auth_required": constants.AUTHORIZATION_REQUIRED,
            "auth_revocable": constants.AUTHORIZATION_REVOCABLE,
            "auth_immutable": constants.AUTHORIZATION_IMMUTABLE,
            "auth_clawback_enabled": constants.AUTHORIZATION_CLAWBACK_ENABLED,
        }

        flags = []
        for key, value in account.raw_data["flags"].items():
            if value:
                flags.append(flags_dict[key])

        return flags

    def get_account_toml(self, public_key: str = None, account: Account = None) -> dict:
        if not account:
            account = self.check_if_account_exists_at_network(public_key=public_key)

        return stellar_toml.fetch_stellar_toml(
            domain=account.raw_data.get("home_domain")
        )

    def get_account_signers(
        self, public_key: str = None, account: Account = None, weight: int = None
    ) -> dict:
        if not account:
            account = self.check_if_account_exists_at_network(public_key=public_key)

        signers: list[dict] = account.raw_data.get("signers", [])

        if weight:
            return [s.get("key") for s in signers if s["weight"] == weight]

        return [s.get("key") for s in signers]

    def get_accounts_by_signer(self, public_key: str) -> list:
        accounts_records = []
        accounts_call_builder = self.server.accounts().for_signer(public_key).limit(100)
        accounts_records += accounts_call_builder.call()["_embedded"]["records"]

        while page_records := accounts_call_builder.next()["_embedded"]["records"]:
            accounts_records += page_records

        return accounts_records
