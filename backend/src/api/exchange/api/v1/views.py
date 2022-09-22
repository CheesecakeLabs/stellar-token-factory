from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.exchange.use_cases import (
    BurnAssetUseCase,
    CreateAssetUseCase,
    CreateClawbackUseCase,
    CreatePaymentUseCase,
    GenerateTOMLUseCase,
    GetAccountOptionsUseCase,
    GetAssetDistributorUseCase,
    GetIssuerInfoUseCase,
    ManageDataUseCase,
    MintAssetUseCase,
    RetrieveTOMLUseCase,
    SetHomeDomainUseCase,
    SetOptionsUseCase,
    SubmitEnvelopeUseCase,
    UpdateAuthorizedFlagUseCase,
)
from api.exchange.utils import get_network

from . import docs, messages
from .serializers import (
    AccountOptionsSerializer,
    BurnAssetRequestSerializer,
    CreateAssetRequestSerializer,
    CreateClawbackRequestSerializer,
    CreateEnvelopeResponseSerializer,
    CreatePaymentRequestSerializer,
    GenerateTOMLSerializer,
    IssuerInfoSerializer,
    ManageDataRequestSerializer,
    MintAssetRequestSerializer,
    PublicKeySerializer,
    SetHomeDomainRequestSerializer,
    SetOptionsRequestSerializer,
    SubmitEnvelopeErrorResponseSerializer,
    SubmitEnvelopeRequestSerializer,
    SubmitEnvelopeSuccessResponseSerializer,
    UpdateAuthorizedFlagRequestSerializer,
)


@extend_schema(**docs.get_issuer_info)
@api_view(("GET",))
def get_issuer_info(request: Request, public_key: str) -> Response:
    data = GetIssuerInfoUseCase().execute(
        network=get_network(request), public_key=public_key
    )

    serializer = IssuerInfoSerializer(data)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.create_asset)
@api_view(("POST",))
def create_asset(request: Request) -> Response:
    serializer = CreateAssetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = CreateAssetUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


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


@extend_schema(**docs.get_asset_distributor)
@api_view(("GET",))
def get_asset_distributor(
    request: Request, asset_code: str, asset_issuer: str
) -> Response:
    distributor_acc: dict = GetAssetDistributorUseCase().execute(
        network=get_network(request), asset_code=asset_code, asset_issuer=asset_issuer
    )

    if not distributor_acc:
        return Response(
            messages.DISTRIBUTOR_NOT_FOUND, status=status.HTTP_404_NOT_FOUND
        )

    serializer = PublicKeySerializer(distributor_acc)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.mint_asset)
@api_view(("POST",))
def mint_asset(request: Request) -> Response:
    serializer = MintAssetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = MintAssetUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.burn_asset)
@api_view(("POST",))
def burn_asset(request: Request) -> Response:
    serializer = BurnAssetRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = BurnAssetUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.create_payment)
@api_view(("POST",))
def create_payment(request: Request) -> Response:
    serializer = CreatePaymentRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = CreatePaymentUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.manage_data)
@api_view(("POST",))
def manage_data(request: Request) -> Response:
    serializer = ManageDataRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = ManageDataUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.create_clawback)
@api_view(("POST",))
def create_clawback(request: Request) -> Response:
    serializer = CreateClawbackRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = CreateClawbackUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.set_authorized_flag)
@api_view(("POST",))
def set_authorized_flag(request: Request) -> Response:
    serializer = UpdateAuthorizedFlagRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = UpdateAuthorizedFlagUseCase().execute(
        network=get_network(request), **serializer.validated_data, clear=False
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.clear_authorized_flag)
@api_view(("POST",))
def clear_authorized_flag(request: Request) -> Response:
    serializer = UpdateAuthorizedFlagRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = UpdateAuthorizedFlagUseCase().execute(
        network=get_network(request), **serializer.validated_data, clear=True
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.set_home_domain)
@api_view(("POST",))
def set_home_domain(request: Request) -> Response:
    serializer = SetHomeDomainRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = SetHomeDomainUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.generate_toml)
@api_view(("POST",))
def generate_toml(request: Request) -> Response:
    serializer = GenerateTOMLSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = GenerateTOMLUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    with NamedTemporaryFile() as toml_file:
        toml_file.write(response.encode())
        toml_file.seek(0)

        response = HttpResponse(toml_file, content_type="application/toml")
        response["Content-Disposition"] = "attachment; filename=stellar.toml"
        return response


@extend_schema(**docs.retrieve_toml)
@api_view(("GET",))
def retrieve_toml(request: Request, asset_issuer: str) -> Response:

    response = RetrieveTOMLUseCase().execute(
        network=get_network(request), public_key=asset_issuer
    )

    serializer = GenerateTOMLSerializer(response)

    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.set_account_options)
@api_view(("POST",))
def set_account_options(request: Request) -> Response:
    serializer = SetOptionsRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    response = SetOptionsUseCase().execute(
        network=get_network(request), **serializer.validated_data
    )

    response_serializer = CreateEnvelopeResponseSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)


@extend_schema(**docs.get_account_options)
@api_view(("GET",))
def get_account_options(request: Request, public_key: str) -> Response:
    response = GetAccountOptionsUseCase().execute(
        network=get_network(request), public_key=public_key
    )

    response_serializer = AccountOptionsSerializer(response)

    return Response(response_serializer.data, status=status.HTTP_200_OK)
