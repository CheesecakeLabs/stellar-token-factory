from drf_spectacular.utils import OpenApiExample, OpenApiTypes
from rest_framework import status

from api.exchange.api.v1 import messages
from api.exchange.api.v1.serializers import (
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
    SubmitEnvelopeRequestSerializer,
    SubmitEnvelopeSuccessResponseSerializer,
    UpdateAuthorizedFlagRequestSerializer,
)

from . import constants

wallets_tag = "Wallets"
assets_tag = "Assets"
transactions_tag = "Transactions"


get_issuer_info = {
    "responses": {
        status.HTTP_200_OK: IssuerInfoSerializer(),
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.ANY,
    },
    "summary": "Get issued assets and flags from an account.",
    "tags": [wallets_tag],
    "examples": [
        OpenApiExample(
            name="Get issuer info",
            status_codes=["200"],
            value=constants.ISSUER_INFO_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Account not found",
            status_codes=["404"],
            value=constants.ACCOUNT_NOT_FOUND_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Invalid public key",
            status_codes=["400"],
            value=constants.INVALID_PUBLIC_KEY_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

create_asset = {
    "request": CreateAssetRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Create a new asset.",
    "description": "Creates an envelope with a trustline of the requested asset for the distributor wallet. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [assets_tag],
    "examples": [
        OpenApiExample(
            name="Create asset envelope successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.CREATE_ASSET_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

submit_envelope = {
    "request": SubmitEnvelopeRequestSerializer,
    "responses": {
        status.HTTP_200_OK: SubmitEnvelopeSuccessResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Submit a envelope to Stellar Network.",
    "tags": [transactions_tag],
    "examples": [
        OpenApiExample(
            name="Envelope submitted successfully.",
            status_codes=["200"],
            value=constants.SUBMIT_ENVELOPE_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing signatures.",
            status_codes=["400"],
            value=constants.SUBMIT_ENVELOPE_MISSING_SIGNATURES_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Operations error.",
            status_codes=["400"],
            value=constants.SUBMIT_ENVELOPE_OP_ERROR_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Invalid envelope XDR.",
            status_codes=["400"],
            value=constants.SUBMIT_ENVELOPE_INVALID_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

get_asset_distributor = {
    "request": None,
    "responses": {
        status.HTTP_200_OK: PublicKeySerializer,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.STR,
    },
    "summary": "Get a distributor wallet public key of an asset.",
    "tags": [assets_tag],
    "examples": [
        OpenApiExample(
            name="Get distributor public key successfully.",
            status_codes=["200"],
            value=constants.PUBLIC_KEY_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Distributor not found.",
            status_codes=["404"],
            value=messages.DISTRIBUTOR_NOT_FOUND,
            request_only=False,
            response_only=True,
        ),
    ],
}

mint_asset = {
    "request": MintAssetRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Mint asset.",
    "description": "Creates an envelope with payment from issuer to distributor. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [assets_tag],
    "examples": [
        OpenApiExample(
            name="Mint asset envelope successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.MINT_ASSET_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

burn_asset = {
    "request": BurnAssetRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Burn asset.",
    "description": "Creates an envelope with payment from distributor to issuer. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [assets_tag],
    "examples": [
        OpenApiExample(
            name="Burn asset envelope successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.BURN_ASSET_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

create_payment = {
    "request": CreatePaymentRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Create a payment transaction.",
    "description": "Creates an envelope with payment from distributor to target. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [transactions_tag],
    "examples": [
        OpenApiExample(
            name="Payment envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.PAYMENT_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

manage_data = {
    "request": ManageDataRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Create a Manage Data transaction.",
    "description": "Creates an envelope with Manage Data in the requested account. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [transactions_tag],
    "examples": [
        OpenApiExample(
            name="Manage Data envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.MANAGE_DATA_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

create_clawback = {
    "request": CreateClawbackRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Create a Clawback transaction.",
    "description": "Creates an envelope with Clawback or Clawback Claimable Balance in the requested account. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [transactions_tag],
    "examples": [
        OpenApiExample(
            name="Create a Clawback envelope.",
            status_codes=["200"],
            value=constants.CLAWBACK_TARGET_REQUEST,
            request_only=True,
            response_only=False,
        ),
        OpenApiExample(
            name="Create a Clawback Claimable Balance envelope.",
            status_codes=["200"],
            value=constants.CLAWBACK_CLAIMABLE_REQUEST,
            request_only=True,
            response_only=False,
        ),
        OpenApiExample(
            name="Clawback envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.CLAWBACK_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

set_authorized_flag = {
    "request": UpdateAuthorizedFlagRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Set Authorized flag of a wallet.",
    "description": "Creates an envelope with Set TrusLine Flags in the requested account to set Authorized flag. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [wallets_tag],
    "examples": [
        OpenApiExample(
            name="Envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.UPDATE_AUTH_FLAG_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

clear_authorized_flag = {
    "request": UpdateAuthorizedFlagRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Clear Authorized flag of a wallet.",
    "description": "Creates an envelope with Set TrusLine Flags in the requested account to remove Authorized flag. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [wallets_tag],
    "examples": [
        OpenApiExample(
            name="Envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.UPDATE_AUTH_FLAG_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

set_home_domain = {
    "request": SetHomeDomainRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Set home domain for an account.",
    "description": "Creates an envelope with Set Options in the requested account to set Home Domain. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [wallets_tag],
    "examples": [
        OpenApiExample(
            name="Envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.SET_HOME_DOMAIN_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}


generate_toml = {
    "request": GenerateTOMLSerializer,
    "responses": {
        status.HTTP_200_OK: OpenApiTypes.BINARY,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
    },
    "summary": "Generate a Stellar TOML.",
    "description": "Generates a Stellar TOML and returns it as a string",
    "tags": [assets_tag],
}


retrieve_toml = {
    "request": None,
    "responses": {
        status.HTTP_200_OK: GenerateTOMLSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.OBJECT,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.OBJECT,
    },
    "summary": "Retrieve a TOML file from an account.",
    "tags": [assets_tag],
    "examples": [
        OpenApiExample(
            name="TOML not found.",
            status_codes=["404"],
            value=constants.TOML_NOT_FOUND_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Account not found.",
            status_codes=["400"],
            value=constants.ACCOUNT_NOT_FOUND_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

set_account_options = {
    "request": SetOptionsRequestSerializer,
    "responses": {
        status.HTTP_200_OK: CreateEnvelopeResponseSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiTypes.ANY,
    },
    "summary": "Set options for an account.",
    "description": "Creates an envelope with Set Options in the requested account to update low Signers and change Clawback/Freeze flags. Changing the signers modifies the thresholds to a default value. The response is the unsigned envelope and the public keys of the required signatures.",
    "tags": [wallets_tag],
    "examples": [
        OpenApiExample(
            name="Envelope created successfully.",
            status_codes=["200"],
            value=constants.ENVELOPE_CREATED_RESPONSE,
            request_only=False,
            response_only=True,
        ),
        OpenApiExample(
            name="Missing required fields.",
            status_codes=["400"],
            value=constants.SET_OPTIONS_MISSING_FIELDS_RESPONSE,
            request_only=False,
            response_only=True,
        ),
    ],
}

get_account_options = {
    "request": None,
    "responses": {
        status.HTTP_200_OK: AccountOptionsSerializer,
        status.HTTP_404_NOT_FOUND: OpenApiTypes.STR,
    },
    "summary": "Get the account options.",
    "tags": [wallets_tag],
}
