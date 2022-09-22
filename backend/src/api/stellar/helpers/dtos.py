from dataclasses import dataclass
from typing import Optional

from stellar_sdk import Account as StellarAccount
from stellar_sdk import Keypair as StellarKeypair


@dataclass
class Keypair:
    public_key: Optional[str]
    secret: Optional[str]

    def __init__(self, public_key: str = None, secret: str = None) -> None:
        if not public_key:
            keypair = StellarKeypair.random()
            public_key = keypair.public_key
            secret = keypair.secret
        elif secret:
            keypair = StellarKeypair.from_secret(secret)
            public_key = keypair.public_key

        self.public_key = public_key
        self.secret = secret


class Account(StellarAccount):
    pass
