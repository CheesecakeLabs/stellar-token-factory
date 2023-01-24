from typing import Any

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser
from stellar_sdk import Keypair, Server

from api.stellar.helpers.transactions import StellarTransaction

USD = "USD"
EUR = "EUR"
NETWORK = "TESTNET"


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.eur_issuer = None
        self.usd_issuer = None
        self.eur_dist = None
        self.usd_dist = None

    def handle(self, *args: list[Any], **options: dict[str, Any]) -> None:
        # Create USD and EUR tokens
        self.usd_issuer, self.usd_dist = self.create_token(USD)
        self.eur_issuer, self.eur_dist = self.create_token(EUR)

        print(
            "USD Issuer: {} - {}".format(
                self.usd_issuer.public_key, self.usd_issuer.secret
            ),
        )
        print(
            "USD Distributor: {} - {}".format(
                self.usd_dist.public_key, self.usd_dist.secret
            ),
        )
        print(
            "EUR Issuer: {} - {}".format(
                self.eur_issuer.public_key, self.eur_issuer.secret
            ),
        )
        print(
            "EUR Distributor: {} - {}".format(
                self.eur_dist.public_key, self.eur_dist.secret
            ),
        )

        # Create main wallet
        main_wallet: Keypair = self.create_main_wallet()
        self.send_token(EUR, main_wallet.public_key, 1000000)
        print(
            "Main wallet: {} - {}".format(main_wallet.public_key, main_wallet.secret),
        )

        # Create the payee wallets
        for index in range(3):
            payee = self.create_payee_wallet()
            print(
                "Payee {}: {} - {}".format(index, payee.public_key, payee.secret),
            )

        # Create offers
        # for index in range(2):
        #     self.create_offer(sell_token_code=USD, buy_token_code=EUR)
        for index in range(2):
            self.create_offer(sell_token_code=EUR, buy_token_code=USD, amount=300000)

    def create_acc_with_friendbot(self):
        keypair = Keypair.random()
        requests.get(f"https://friendbot.stellar.org?addr={keypair.public_key}")
        return keypair

    def create_token(self, code: str) -> tuple:
        issuer_kp = self.create_acc_with_friendbot()
        distributor_kp = self.create_acc_with_friendbot()

        # Change trust transaction
        self.change_trust(code, distributor_kp, issuer_kp)

        # Payment transaction
        stellar = StellarTransaction(NETWORK, issuer_kp.public_key)
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

        self.change_trust(USD, wallet_kp)

        return wallet_kp

    def create_main_wallet(self) -> Keypair:
        wallet_kp = self.create_acc_with_friendbot()

        # Change trustline
        self.change_trust(EUR, wallet_kp)

        return wallet_kp

    def create_offer(
        self, sell_token_code: str, buy_token_code: str, amount: float
    ) -> Keypair:
        wallet_kp = self.create_acc_with_friendbot()

        if sell_token_code == EUR:
            sell_issuer = self.eur_issuer
            buy_issuer = self.usd_issuer
        else:
            sell_issuer = self.usd_issuer
            buy_issuer = self.eur_issuer

        # Change trustlines
        self.change_trust(sell_token_code, wallet_kp)
        self.change_trust(buy_token_code, wallet_kp)

        # Get some tokens
        self.send_token(sell_token_code, wallet_kp.public_key, amount)

        stellar = StellarTransaction(NETWORK, wallet_kp.public_key)
        transaction_builder = stellar.append_manage_sell_offer(
            amount=str(amount),
            sell_asset_code=sell_token_code,
            sell_issuer_public_key=sell_issuer.public_key,
            buy_asset_code=buy_token_code,
            buy_issuer_public_key=buy_issuer.public_key,
            price=0.92,
            offer_id=0,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[wallet_kp.secret]
        )
        stellar.submit_transaction(transaction_envelope)

        return wallet_kp

    def send_token(self, token_code: str, to: str, amount: float) -> None:
        if token_code == EUR:
            issuer_kp = self.eur_issuer
            dist_kp = self.eur_dist
        else:
            issuer_kp = self.usd_issuer
            dist_kp = self.usd_dist

        stellar = StellarTransaction(NETWORK, dist_kp.public_key)
        transaction_builder = stellar.append_payment_operation(
            destination_public_key=to,
            amount=str(amount),
            asset_code=token_code,
            asset_issuer=issuer_kp.public_key,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[dist_kp.secret]
        )
        stellar.submit_transaction(transaction_envelope)

    def change_trust(self, token_code: str, _from: str, issuer: Keypair = None) -> None:
        issuer = issuer or (self.eur_issuer if token_code == EUR else self.usd_issuer)
        # Change trustline
        stellar = StellarTransaction(NETWORK, _from.public_key)
        transaction_builder = stellar.append_change_trust_operation(
            asset_code=token_code,
            asset_issuer=issuer.public_key,
        )
        transaction_envelope = stellar.build_transaction(transaction_builder)
        transaction_envelope = stellar.sign_transaction(
            envelope=transaction_envelope, signatures=[_from.secret]
        )
        stellar.submit_transaction(transaction_envelope)
