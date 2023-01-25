from rest_framework import status

from .serializers import BalanceSerializer, PayeeSerializer

demo_tag = "Demo"


get_payees_list = {
    "responses": {
        status.HTTP_200_OK: PayeeSerializer(many=True),
    },
    "summary": "Get payees list.",
    "tags": [demo_tag],
}

get_main_wallet_eur_balance = {
    "responses": {
        status.HTTP_200_OK: BalanceSerializer(),
    },
    "summary": "Get main wallet EUR balance",
    "tags": [demo_tag],
}
