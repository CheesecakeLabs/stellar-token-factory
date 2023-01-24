from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.exchange.use_cases.demo import GetPayeesListUseCase

from . import docs
from .serializers import PayeeSerializer


@extend_schema(**docs.get_payees_list)
@api_view(("GET",))
def get_payees_list(request: Request) -> Response:
    response = GetPayeesListUseCase().execute()

    serializer = PayeeSerializer(response, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
