from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import (
    ACCOUNT_NOT_FOUND,
    INVALID_ISSUER_PUBLIC_KEY,
    INVALID_NETWORK,
    TOML_NOT_FOUND,
    BusinessException,
)
from api.core.use_cases.base import BaseUseCase
from api.stellar.helpers.accounts import StellarAccount
from api.stellar.helpers.exceptions import AccountNotFoundAtNetwork, InvalidNetwork


class RetrieveTOMLUseCase(BaseUseCase):
    def execute(
        self,
        network: str,
        public_key: str,
    ) -> str:
        """
        Retrieve a Stellar TOML file from an account
        Params:
            network: Current network (TESTNET or PUBLIC)
            public_key: Account public key
        """

        # Check if public key is valid
        try:
            StellarAccount.validate_public_key(public_key=public_key)
        except:
            raise BusinessException(
                INVALID_ISSUER_PUBLIC_KEY, status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check if network is valid
        try:
            stellar = StellarAccount(network=network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            toml_raw_data = stellar.get_account_toml(public_key=public_key)
        except AccountNotFoundAtNetwork:
            raise BusinessException(
                ACCOUNT_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )
        except:
            raise BusinessException(
                TOML_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND
            )

        toml_data = {}
        toml_data["currency_doc"] = toml_raw_data.pop("CURRENCIES", [])
        toml_data["point_of_contact_doc"] = toml_raw_data.pop("PRINCIPALS", [])
        toml_data["org_doc"] = toml_raw_data.pop("DOCUMENTATION", {})
        toml_data["general_info"] = toml_raw_data

        return toml_data
