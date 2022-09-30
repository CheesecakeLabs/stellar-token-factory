from typing import Union

from rest_framework import status

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_NETWORK,
    INVALID_PUBLIC_KEY,
    BusinessException,
)
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.transactions import StellarTransaction

from .base import BaseUseCase


class BaseStellarUseCase(BaseUseCase):
    def _validate_public_key(
        self, public_key: str, error: int = INVALID_PUBLIC_KEY
    ) -> None:
        try:
            StellarTransaction.validate_public_key(public_key=public_key)
        except:
            raise BusinessException(error, status_code=status.HTTP_400_BAD_REQUEST)

    def _get_stellar_transaction_class(
        self,
        network: str,
        source_public_key: str = None,
        source_public_key_error: int = ACCOUNT_NOT_FOUND,
    ) -> None:
        try:
            return StellarTransaction(
                network=network, source_public_key=source_public_key
            )
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )
        except:
            raise BusinessException(
                source_public_key_error, status_code=status.HTTP_404_NOT_FOUND
            )

    def _get_stellar_account_class(self, network: str) -> None:
        try:
            return StellarAccount(network=network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

    def _check_if_account_exists_at_network(
        self,
        stellar_class: Union[StellarTransaction, StellarAccount],
        public_key: str,
        error: int = ACCOUNT_NOT_FOUND,
    ) -> None:
        try:
            return stellar_class.check_if_account_exists_at_network(
                public_key=public_key
            )
        except:
            raise BusinessException(error, status_code=status.HTTP_404_NOT_FOUND)
