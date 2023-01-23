from django.conf import settings
from django.utils.translation import gettext_lazy as _

from api.core.use_cases.base import BaseUseCase

COMPANIES_INFO = [
    {
        "name": "McCullough Ltd",
        "address": "34 Blades Dr, New Madrid, Missouri (MO)",
        "phone": "202-555-0110",
        "bank_account": "343020630386179",
    },
    {
        "name": "ACME Technologies Inc.",
        "address": "68 Dakota St, San Francisco, California (CA)",
        "phone": "805-555-0196",
        "bank_account": "5568285118798859",
    },
    {
        "name": "Ziemann-Mills",
        "address": "2735 Initial Pl, Enumclaw, Washington (WA)",
        "phone": "701-555-0114",
        "bank_account": "4418496088769771",
    },
    {
        "name": "Wyman LLC",
        "address": "6701 Johnson Ln, Fordoche, Louisiana (LA)",
        "phone": "207-555-0188",
        "bank_account": "3536885221739924",
    },
    {
        "name": "Opentech",
        "address": "501 Norris St, Norristown, Pennsylvania (PA)",
        "phone": "701-555-0198",
        "bank_account": "4293315080431109",
    },
    {
        "name": "Green-plus",
        "address": "541 Camino Dr, Santa Clara, California (CA)",
        "phone": "805-555-0146",
        "bank_account": "376832454893811",
    },
]


class GetPayeesListUseCase(BaseUseCase):
    def execute(self) -> dict:
        """
        Get payees list
        """
        payees = []
        companies_len = len(COMPANIES_INFO)
        for index, account in enumerate(settings.PAYEES_LIST):
            company_index = index % companies_len
            COMPANIES_INFO[company_index]["stellar_wallet"] = account
            payees.append(COMPANIES_INFO[company_index])

        return payees
