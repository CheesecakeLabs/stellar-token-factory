from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.exchange.use_cases.demo import GetMainWalletBalance, GetPayeesListUseCase

from . import docs
from .serializers import BalanceSerializer, PayeeSerializer


@extend_schema(**docs.get_payees_list)
@api_view(("GET",))
def get_payees_list(request: Request) -> Response:
    response = GetPayeesListUseCase().execute()

    serializer = PayeeSerializer(response, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.get_main_wallet_eur_balance)
@api_view(("GET",))
def get_main_wallet_eur_balance(request: Request) -> Response:
    response = GetMainWalletBalance().execute(
        network="TESTNET",
        asset_code=settings.EUR_CODE,
        asset_issuer=settings.EUR_ISSUER,
    )

    if not response:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BalanceSerializer(response)

    return Response(serializer.data, status=status.HTTP_200_OK)
