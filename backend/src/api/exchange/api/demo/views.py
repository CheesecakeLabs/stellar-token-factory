from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.exchange.use_cases.demo import (
    CreatePathPaymentStrictReceiveUseCase,
    GetPayeesListUseCase,
)

from . import docs
from .serializers import (
    CreatePathPaymentStrictReceiveSerializer,
    EnvelopeXDRSerializer,
    PayeeSerializer,
)


@extend_schema(**docs.get_payees_list)
@api_view(("GET",))
def get_payees_list(request: Request) -> Response:
    response = GetPayeesListUseCase().execute()

    serializer = PayeeSerializer(response, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.get_payees_list)
@api_view(("POST",))
def create_path_payment_strict_receive_envelope(request: Request) -> Response:
    serializer = CreatePathPaymentStrictReceiveSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = CreatePathPaymentStrictReceiveUseCase().execute(
        network="TESTNET", **serializer.validated_data
    )

    serializer = EnvelopeXDRSerializer(response)

    return Response(serializer.data, status=status.HTTP_200_OK)
