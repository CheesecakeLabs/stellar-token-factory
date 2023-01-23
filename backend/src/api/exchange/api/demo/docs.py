from rest_framework import status

from .serializers import PayeeSerializer

demo_tag = "Demo"


get_payees_list = {
    "responses": {
        status.HTTP_200_OK: PayeeSerializer(many=True),
    },
    "summary": "Get payees list.",
    "tags": [demo_tag],
}
