from django.utils.translation import gettext_lazy as _
from rest_framework import status

from api.core.helpers.business_errors import TOML_NOT_FOUND, BusinessException
from api.core.use_cases.base_stellar import BaseStellarUseCase


class RetrieveTOMLUseCase(BaseStellarUseCase):
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
        self._validate_public_key(public_key)

        stellar = self._get_stellar_account_class(network)

        account = self._check_if_account_exists_at_network(stellar, public_key)

        try:
            toml_raw_data = stellar.get_account_toml(account=account)
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
