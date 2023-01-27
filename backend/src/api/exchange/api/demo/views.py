from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.exchange.api.v1.serializers import (
    SubmitEnvelopeErrorResponseSerializer,
    SubmitEnvelopeSuccessResponseSerializer,
)
from api.exchange.use_cases.demo import (
    CreatePathPaymentStrictReceiveUseCase,
    GetMainWalletBalance,
    GetPayeesListUseCase,
    SubmitEnvelopeUseCase,
)
from api.exchange.utils import get_network

from . import docs
from .serializers import (
    BalanceSerializer,
    PathPaymentStrictReceiveRequestSerializer,
    PathPaymentStrictReceiveResponseSerializer,
    PayeeSerializer,
    SubmitEnvelopeRequestSerializer,
)


@extend_schema(**docs.get_payees_list)
@api_view(("GET",))
def get_payees_list(request: Request) -> Response:
    response = GetPayeesListUseCase().execute()

    serializer = PayeeSerializer(response, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.create_path_payment_strict_receive_envelope)
@api_view(("POST",))
def create_path_payment_strict_receive_envelope(request: Request) -> Response:
    network: str = get_network(request)

    serializer = PathPaymentStrictReceiveRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = CreatePathPaymentStrictReceiveUseCase().execute(
        network=network, **serializer.validated_data
    )

    serializer = PathPaymentStrictReceiveResponseSerializer(response)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.get_main_wallet_eur_balance)
@api_view(("GET",))
def get_main_wallet_eur_balance(request: Request) -> Response:
    network: str = get_network(request)

    response = GetMainWalletBalance().execute(
        network=network,
        asset_code=settings.EUR_CODE,
        asset_issuer=settings.EUR_ISSUER,
    )

    if not response:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BalanceSerializer(response)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.submit_envelope)
@api_view(("POST",))
def submit_envelope(request: Request) -> Response:
    serializer = SubmitEnvelopeRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    network: str = get_network(request)
    response = SubmitEnvelopeUseCase().execute(
        network=network, **serializer.validated_data
    )
    if response.get("success"):
        serializer = SubmitEnvelopeSuccessResponseSerializer(
            response, context={"network": network}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = SubmitEnvelopeErrorResponseSerializer(response)
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
