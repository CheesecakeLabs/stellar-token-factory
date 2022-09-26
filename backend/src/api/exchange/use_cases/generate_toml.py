from collections import OrderedDict
from typing import List, Union

import toml
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from toml.ordered import TomlOrderedEncoder

from api.core.helpers.business_errors import INVALID_NETWORK, BusinessException
from api.core.use_cases.base_stellar import BaseStellarUseCase
from api.stellar.helpers.exceptions import InvalidNetwork
from api.stellar.helpers.utils import get_network_data


class GenerateTOMLUseCase(BaseStellarUseCase):
    def execute(
        self,
        network: str,
        general_info: dict[str, Union[str, List[str]]] = {},
        org_doc: dict[str, str] = {},
        point_of_contact_doc: List[dict[str, str]] = [],
        currency_doc: List[dict[str, Union[str, int, bool, List[str]]]] = [],
    ) -> str:
        """
        Generate a Stellar TOML file
        Params:
            network: Current network (TESTNET or PUBLIC)
            general_info: Global fields in the Stellar TOML
            org_doc: [DOCUMENTATION] table in the Stellar TOML
            point_of_contact_doc: [[PRINCIPALS]] list in the Stellar TOML
            currency_doc: [[CURRENCIES]] list in the Stellar TOML
        """
        try:
            network_data = get_network_data(network)
        except InvalidNetwork:
            raise BusinessException(
                INVALID_NETWORK, status_code=status.HTTP_400_BAD_REQUEST
            )

        toml_obj = OrderedDict()
        toml_obj["VERSION"] = settings.STELLAR_TOML_VERSION
        toml_obj["NETWORK_PASSPHRASE"] = network_data.get("passphrase")
        toml_obj.update(general_info)

        if org_doc:
            toml_obj["DOCUMENTATION"] = org_doc
        if point_of_contact_doc:
            toml_obj["PRINCIPALS"] = point_of_contact_doc
        if currency_doc:
            toml_obj["CURRENCIES"] = currency_doc

        toml_str = toml.dumps(toml_obj, encoder=TomlOrderedEncoder())

        return toml_str
