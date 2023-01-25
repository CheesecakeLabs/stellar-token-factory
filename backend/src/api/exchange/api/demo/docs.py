from rest_framework import status

from .serializers import (
    PathPaymentStrictReceiveRequestSerializer,
    PathPaymentStrictReceiveResponseSerializer,
    PayeeSerializer,
)

demo_tag = "Demo"


get_payees_list = {
    "responses": {
        status.HTTP_200_OK: PayeeSerializer(many=True),
    },
    "summary": "Get payees list.",
    "tags": [demo_tag],
}

create_path_payment_strict_receive_envelope = {
    "request": PathPaymentStrictReceiveRequestSerializer,
    "responses": {
        status.HTTP_200_OK: PathPaymentStrictReceiveResponseSerializer(),
    },
    "summary": "Create path payment strict receive envelope (EUR -> USD).",
    "tags": [demo_tag],
}
