from django.test import override_settings

from api.exchange.use_cases.demo import GetPayeesListUseCase

from .mocks import constants


@override_settings(PAYEES_LIST=constants.PAYEES_LIST)
def test_get_payees_list_succesfully():
    response: list = GetPayeesListUseCase().execute()

    assert response == [
        {
            "name": "McCullough Ltd",
            "address": "34 Blades Dr, New Madrid, Missouri (MO)",
            "phone": "202-555-0110",
            "bank_account": "343020630386179",
            "stellar_wallet": "GC27BXCORFXR4JLVPWVZXXALHWICY7YF5B3UN76RPRGFGQAK5LOVNL6E",
        },
        {
            "name": "ACME Technologies Inc.",
            "address": "68 Dakota St, San Francisco, California (CA)",
            "phone": "805-555-0196",
            "bank_account": "5568285118798859",
            "stellar_wallet": "GCONTCA4CM6EBCIJATWTLEPI52ZOFXT7STWZ6WOYZU7ZON6SXYHABJ3K",
        },
        {
            "name": "Ziemann-Mills",
            "address": "2735 Initial Pl, Enumclaw, Washington (WA)",
            "phone": "701-555-0114",
            "bank_account": "4418496088769771",
            "stellar_wallet": "GCU6AOSXXERDXMR4FEKUWOKNITGCHJ6VRSIVHNGNB4OYMOHL2DBWPCNC",
        },
        {
            "name": "Wyman LLC",
            "address": "6701 Johnson Ln, Fordoche, Louisiana (LA)",
            "phone": "207-555-0188",
            "bank_account": "3536885221739924",
            "stellar_wallet": "GDQTU4W3UFE73VCEJ4SLISP3KLM36AYQWXLAKKDI4FOJ7T5ZBQHZVXHU",
        },
        {
            "name": "Opentech",
            "address": "501 Norris St, Norristown, Pennsylvania (PA)",
            "phone": "701-555-0198",
            "bank_account": "4293315080431109",
            "stellar_wallet": "GB6QNWJI4ERDKF3HPJOGHXN7IY5WE3BOIUGPSHJWPJSCLKQUQ57O5YFS",
        },
        {
            "name": "Green-plus",
            "address": "541 Camino Dr, Santa Clara, California (CA)",
            "phone": "805-555-0146",
            "bank_account": "376832454893811",
            "stellar_wallet": "GA3ABN3IJ2RKWWJVZDLPUUGRMDBBS23EIHPRBYAALLII2CAE5JAF7X36",
        },
    ]
