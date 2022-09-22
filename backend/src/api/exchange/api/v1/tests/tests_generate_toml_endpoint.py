import json

import pytest
from django.test.client import Client
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from api.exchange.api.v1.serializers import GenerateTOMLSerializer

from .mocks.constants import (
    GENERATE_TOML_FAIL_RESPONSES,
    GENERATE_TOML_SUCCESS_RESPONSES,
)


def post_generate_toml_request(
    client: Client, network: str = None, **kwargs
) -> Response:
    """
    Make a request to set options
    Args:
        client: HTTP Client
    """
    return client.post(
        path=reverse("exchange:generate-toml"),
        data=json.dumps(kwargs),
        content_type="application/json",
        headers={"network": network},
    )


def test_generate_toml_request_serializer() -> None:
    request = {
        "general_info": {
            "federation_server": "https://domain.org",
            "auth_server": "https://domain.org",
            "transfer_server": "https://domain.org",
            "transfer_server_sep24": "https://domain.org",
            "kyc_server": "https://domain.org",
            "web_auth_endpoint": "https://domain.org",
            "signing_key": "string",
            "horizon_url": "http://domain.org",
            "accounts": ["string"],
            "uri_request_signing_key": "string",
            "direct_payment_server": "https://domain.org",
            "anchor_quote_server": "https://domain.org",
        },
        "org_doc": {
            "name": "string",
            "dba": "string",
            "url": "https://domain.org",
            "logo": "http://domain.org",
            "description": "string",
            "physical_address": "string",
            "physical_address_attestation": "https://domain.org",
            "phone_number": "string",
            "phone_number_attestation": "https://domain.org",
            "keybase": "string",
            "twitter": "string",
            "github": "string",
            "official_email": "string",
            "support_email": "string",
            "licensing_authority": "string",
            "license_type": "string",
            "license_number": "string",
        },
        "point_of_contact_doc": [
            {
                "name": "string",
                "email": "string",
                "keybase": "string",
                "telegram": "string",
                "twitter": "string",
                "github": "string",
                "id_photo_hash": "string",
                "verification_photo_hash": "string",
            }
        ],
        "currency_doc": [
            {
                "code": "string",
                "code_template": "string",
                "issuer": "string",
                "status": "live",
                "display_decimals": 0,
                "name": "string",
                "description": "string",
                "conditions": "string",
                "image": "http://domain.org",
                "fixed_number": 0,
                "max_number": 0,
                "is_unlimited": True,
                "is_asset_anchored": True,
                "anchor_asset_type": "fiat",
                "anchor_asset": "string",
                "attestation_of_reserve": "https://domain.org",
                "redemption_instructions": "string",
                "collateral_addresses": ["string"],
                "collateral_address_messages": ["string"],
                "collateral_address_signatures": ["string"],
                "regulated": False,
                "approval_server": "https://domain.org",
                "approval_criteria": "string",
            }
        ],
    }

    serializer = GenerateTOMLSerializer(data=request)
    assert serializer.is_valid()
    assert serializer.validated_data == {
        "general_info": {
            "FEDERATION_SERVER": "https://domain.org",
            "AUTH_SERVER": "https://domain.org",
            "TRANSFER_SERVER": "https://domain.org",
            "TRANSFER_SERVER_SEP0024": "https://domain.org",
            "KYC_SERVER": "https://domain.org",
            "WEB_AUTH_ENDPOINT": "https://domain.org",
            "SIGNING_KEY": "string",
            "HORIZON_URL": "http://domain.org",
            "ACCOUNTS": ["string"],
            "URI_REQUEST_SIGNING_KEY": "string",
            "DIRECT_PAYMENT_SERVER": "https://domain.org",
            "ANCHOR_QUOTE_SERVER": "https://domain.org",
        },
        "org_doc": {
            "ORG_NAME": "string",
            "ORG_DBA": "string",
            "ORG_URL": "https://domain.org",
            "ORG_LOGO": "http://domain.org",
            "ORG_DESCRIPTION": "string",
            "ORG_PHYSICAL_ADDRESS": "string",
            "ORG_PHYSICAL_ADDRESS_ATTESTATION": "https://domain.org",
            "ORG_PHONE_NUMBER": "string",
            "ORG_PHONE_NUMBER_ATTESTATION": "https://domain.org",
            "ORG_KEYBASE": "string",
            "ORG_TWITTER": "string",
            "ORG_GITHUB": "string",
            "ORG_OFFICIAL_EMAIL": "string",
            "ORG_SUPPORT_EMAIL": "string",
            "ORG_LICENSING_AUTHORITY": "string",
            "ORG_LICENSE_TYPE": "string",
            "ORG_LICENSE_NUMBER": "string",
        },
        "point_of_contact_doc": [
            {
                "name": "string",
                "email": "string",
                "keybase": "string",
                "telegram": "string",
                "twitter": "string",
                "github": "string",
                "id_photo_hash": "string",
                "verification_photo_hash": "string",
            }
        ],
        "currency_doc": [
            {
                "code": "string",
                "code_template": "string",
                "issuer": "string",
                "status": "live",
                "display_decimals": 0,
                "name": "string",
                "desc": "string",
                "conditions": "string",
                "image": "http://domain.org",
                "fixed_number": 0,
                "max_number": 0,
                "is_unlimited": True,
                "is_asset_anchored": True,
                "anchor_asset_type": "fiat",
                "anchor_asset": "string",
                "attestation_of_reserve": "https://domain.org",
                "redemption_instructions": "string",
                "collateral_addresses": ["string"],
                "collateral_address_messages": ["string"],
                "collateral_address_signatures": ["string"],
                "regulated": False,
                "approval_server": "https://domain.org",
                "approval_criteria": "string",
            }
        ],
    }


@pytest.mark.parametrize(
    "request_data,expected_response", GENERATE_TOML_SUCCESS_RESPONSES
)
def test_generate_toml_successfully(
    client: Client, request_data: dict, expected_response: str
) -> None:
    response = post_generate_toml_request(client=client, **request_data)

    assert response.status_code == status.HTTP_200_OK
    response.content_type = "application/toml"

    assert response.content.decode() == expected_response


@pytest.mark.parametrize("request_data,error", GENERATE_TOML_FAIL_RESPONSES)
def test_generate_toml_fails_when_request_data_is_wrong(
    client: Client, request_data: dict, error: dict
):
    response = post_generate_toml_request(client, **request_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == error
