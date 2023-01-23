from typing import Any

import requests
from api.stellar.helpers.transactions import StellarTransaction
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser
from stellar_sdk import Keypair, Server

USD = "USD"
EUR = "EUR"


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eur_issuer = None
        self.usd_issuer = None
        self.payees = []

    def handle(self, *args: list[Any], **options: dict[str, Any]) -> None:
        # Create USD and EUR tokens
        self.usd_issuer, usd_dist = self.mint_token(USD)
        self.eur_issuer, eur_dist = self.mint_token(EUR)

        print(
            "USD Issuer: {} - {}".format(
                self.usd_issuer.public_key, self.usd_issuer.secret
            ),
        )
        print(
            "USD Distributor: {} - {}".format(usd_dist.public_key, usd_dist.secret),
        )
        print(
            "EUR Issuer: {} - {}".format(
                self.eur_issuer.public_key, self.eur_issuer.secret
            ),
        )
        print(
            "EUR Distributor: {} - {}".format(eur_dist.public_key, eur_dist.secret),
        )

        # Create the payee wallets
        for _ in range(3):
            self.payees.append(self.create_payee_wallet())
        print(self.payees)

    def create_acc_with_friendbot(self):
        keypair = Keypair.random()
        requests.get(f"https://friendbot.stellar.org?addr={keypair.public_key}")
        return keypair

    def mint_token(self, code: str) -> tuple:
        issuer_kp = self.create_acc_with_friendbot()
        distributor_kp = self.create_acc_with_friendbot()

        # Change trust transaction
        stellar = StellarTransaction("TESTNET", distributor_kp.public_key)
        transaction_builder = stellar.append_change_trust_operation(
            asset_code=code,
            asset_issuer=issuer_kp.public_key,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[distributor_kp.secret]
        )
        stellar.submit_transaction(transaction_envelope)

        # Payment transaction
        stellar = StellarTransaction("TESTNET", issuer_kp.public_key)
        transaction_builder = stellar.append_payment_operation(
            destination_public_key=distributor_kp.public_key,
            amount="10000000000",
            asset_code=code,
            asset_issuer=issuer_kp.public_key,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[issuer_kp.secret]
        )
        stellar.submit_transaction(transaction_envelope)

        return issuer_kp, distributor_kp

    def create_payee_wallet(self) -> Keypair:
        wallet_kp = self.create_acc_with_friendbot()

        stellar = StellarTransaction("TESTNET", wallet_kp.public_key)
        transaction_builder = stellar.append_change_trust_operation(
            asset_code=USD,
            asset_issuer=self.usd_issuer.public_key,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[wallet_kp.secret]
        )
        stellar.submit_transaction(transaction_envelope)
        return wallet_kp
