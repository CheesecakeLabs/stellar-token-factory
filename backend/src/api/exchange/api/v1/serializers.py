from collections import OrderedDict

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from api.core.helpers.serializers import NonEmptySerializer
from api.core.helpers.validators import GreaterThanValidator, HTTPSValidator

STELLAR_KEY_MAX_LENGTH = 56
STELLAR_CODE_MAX_LENGTH = 12
LIMIT_MAX_VALUE = 922337203685
CLAWBACK_ID_MAX_LENGTH = 10000
MEMO_TEXT_MAX_LENGTH = 28
HOME_DOMAIN_MAX_LENGHT = 32


class AssetSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=STELLAR_CODE_MAX_LENGTH, source="asset_code"
    )
    issuer = serializers.CharField(
        max_length=STELLAR_KEY_MAX_LENGTH, source="asset_issuer"
    )
    supply = serializers.FloatField(min_value=0, source="amount")
    name = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.CharField)
    def get_name(self, data):
        return f"{data.get('asset_code')}-{data.get('asset_issuer')}"


class IssuerInfoSerializer(serializers.Serializer):
    clawback = serializers.BooleanField()
    freeze = serializers.BooleanField()
    assets = AssetSerializer(many=True, read_only=True)


class CreateAssetRequestSerializer(serializers.Serializer):
    issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    distributor = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    asset_code = serializers.CharField(max_length=STELLAR_CODE_MAX_LENGTH)
    limit = serializers.FloatField(
        validators=[GreaterThanValidator(0)],
        max_value=LIMIT_MAX_VALUE,
        required=False,
        allow_null=True,
    )


class CreateEnvelopeResponseSerializer(serializers.Serializer):
    envelope_xdr = serializers.CharField(max_length=10000)
    required_signatures = serializers.ListField(
        child=serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    )


class SubmitEnvelopeRequestSerializer(serializers.Serializer):
    envelope_xdr = serializers.CharField(max_length=10000)


class SubmitEnvelopeSuccessResponseSerializer(serializers.Serializer):
    transaction_hash = serializers.SerializerMethodField(read_only=True)
    transaction_link = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.CharField)
    def get_transaction_hash(self, data):
        return data.get("details").get("hash")

    @extend_schema_field(serializers.CharField)
    def get_transaction_link(self, data):
        tx_hash = data.get("details").get("hash")
        server = self.context.get("network", "testnet").lower()
        return f"https://stellar.expert/explorer/{server}/tx/{tx_hash}"


class SubmitEnvelopeErrorResponseSerializer(serializers.Serializer):
    stellar_status_code = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(serializers.CharField)
    def get_message(self, data):
        return data.get("details").get("message")

    @extend_schema_field(serializers.IntegerField)
    def get_stellar_status_code(self, data):
        return data.get("details").get("status")


class PublicKeySerializer(serializers.Serializer):
    public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)


class MintAssetRequestSerializer(serializers.Serializer):
    issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    distributor = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    asset_code = serializers.CharField(max_length=STELLAR_CODE_MAX_LENGTH)
    amount = serializers.FloatField(validators=[GreaterThanValidator(0)])


class BurnAssetRequestSerializer(MintAssetRequestSerializer):
    pass


class CreatePaymentRequestSerializer(MintAssetRequestSerializer):
    target = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)


class ManageDataRequestSerializer(serializers.Serializer):
    public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    name = serializers.CharField(max_length=64)
    value = serializers.CharField(
        max_length=64,
        required=False,
        allow_null=True,
    )


class CreateClawbackRequestSerializer(serializers.Serializer):
    issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    asset_code = serializers.CharField(
        max_length=STELLAR_CODE_MAX_LENGTH,
        required=False,
        allow_null=True,
    )
    amount = serializers.FloatField(
        validators=[GreaterThanValidator(0)],
        required=False,
        allow_null=True,
    )
    target = serializers.CharField(
        max_length=STELLAR_KEY_MAX_LENGTH,
        required=False,
        allow_null=True,
    )
    claimable_id = serializers.CharField(
        max_length=CLAWBACK_ID_MAX_LENGTH,
        required=False,
        allow_null=True,
    )

    def validate(self, data: OrderedDict):
        if data.get("target"):
            if data.get("claimable_id"):
                raise serializers.ValidationError(
                    {
                        "target": _(
                            "This field must not be filled when Claimable ID has value."
                        ),
                        "claimable_id": _(
                            "This field must not be filled when Target has value"
                        ),
                    }
                )

            errors = {}
            for field in ["asset_code", "amount"]:
                if not data.get(field):
                    errors.update(
                        {
                            field: _("This field is required."),
                        }
                    )

            if errors:
                raise serializers.ValidationError(errors)

        elif not data.get("claimable_id"):
            raise serializers.ValidationError(
                {
                    "target": _("This field is required when Claimable ID is null."),
                    "claimable_id": _("This field is required when Target is null."),
                }
            )

        return data


class UpdateAuthorizedFlagRequestSerializer(serializers.Serializer):
    issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    asset_code = serializers.CharField(max_length=STELLAR_CODE_MAX_LENGTH)
    target = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    memo_text = serializers.CharField(
        max_length=MEMO_TEXT_MAX_LENGTH,
        required=False,
        allow_null=True,
    )


class SetHomeDomainRequestSerializer(serializers.Serializer):
    public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    home_domain = serializers.CharField(max_length=HOME_DOMAIN_MAX_LENGHT)

    def validate(self, data: OrderedDict):
        home_domain: str = data.get("home_domain")
        if home_domain.startswith(("http://", "https://")):
            raise serializers.ValidationError(
                {
                    "home_domain": _(
                        "Only domain name is accepted (without HTTP ou HTTPS)."
                    )
                }
            )

        return data


class TOMLGeneralInfo(NonEmptySerializer):
    federation_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="FEDERATION_SERVER",
    )
    auth_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="AUTH_SERVER",
    )
    transfer_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        source="TRANSFER_SERVER",
        allow_blank=True,
    )
    transfer_server_sep24 = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="TRANSFER_SERVER_SEP0024",
    )
    kyc_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="KYC_SERVER",
    )
    web_auth_endpoint = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="WEB_AUTH_ENDPOINT",
    )
    signing_key = serializers.CharField(
        max_length=STELLAR_KEY_MAX_LENGTH,
        required=False,
        allow_null=True,
        allow_blank=True,
        source="SIGNING_KEY",
    )
    horizon_url = serializers.URLField(
        required=False, allow_null=True, allow_blank=True, source="HORIZON_URL"
    )
    accounts = serializers.ListField(
        child=serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH),
        required=False,
        source="ACCOUNTS",
        allow_null=True,
    )
    uri_request_signing_key = serializers.CharField(
        max_length=STELLAR_KEY_MAX_LENGTH,
        required=False,
        allow_null=True,
        allow_blank=True,
        source="URI_REQUEST_SIGNING_KEY",
    )
    direct_payment_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="DIRECT_PAYMENT_SERVER",
    )
    anchor_quote_server = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="ANCHOR_QUOTE_SERVER",
    )


class TOMLOrganizationDoc(NonEmptySerializer):
    name = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_NAME"
    )
    dba = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_DBA"
    )
    url = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="ORG_URL",
    )
    logo = serializers.URLField(
        required=False, allow_null=True, allow_blank=True, source="ORG_LOGO"
    )
    description = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_DESCRIPTION"
    )
    physical_address = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_PHYSICAL_ADDRESS"
    )
    physical_address_attestation = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="ORG_PHYSICAL_ADDRESS_ATTESTATION",
    )
    phone_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_PHONE_NUMBER"
    )
    phone_number_attestation = serializers.URLField(
        validators=[HTTPSValidator],
        required=False,
        allow_null=True,
        allow_blank=True,
        source="ORG_PHONE_NUMBER_ATTESTATION",
    )
    keybase = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_KEYBASE"
    )
    twitter = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_TWITTER"
    )
    github = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_GITHUB"
    )
    official_email = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_OFFICIAL_EMAIL"
    )
    support_email = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_SUPPORT_EMAIL"
    )
    licensing_authority = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        source="ORG_LICENSING_AUTHORITY",
    )
    license_type = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_LICENSE_TYPE"
    )
    license_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, source="ORG_LICENSE_NUMBER"
    )


class TOMLPointOfContactDoc(NonEmptySerializer):
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    keybase = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    telegram = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    twitter = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    github = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    id_photo_hash = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    verification_photo_hash = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class TOMLCurrencyDoc(NonEmptySerializer):
    STATUS_CHOICES = ["live", "dead", "test", "private"]
    ANCHOR_ASSET_TYPE_CHOICES = [
        "fiat",
        "crypto",
        "nft",
        "stock",
        "bond",
        "commodity",
        "realestate",
        "other",
    ]

    code = serializers.CharField(
        max_length=STELLAR_CODE_MAX_LENGTH,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    code_template = serializers.CharField(
        max_length=12, required=False, allow_blank=True, allow_null=True
    )
    issuer = serializers.CharField(
        max_length=STELLAR_KEY_MAX_LENGTH,
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    status = serializers.ChoiceField(
        required=False, allow_blank=True, allow_null=True, choices=STATUS_CHOICES
    )
    display_decimals = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=7,
        allow_null=True,
    )
    name = serializers.CharField(
        max_length=20, required=False, allow_blank=True, allow_null=True
    )
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, source="desc"
    )
    conditions = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    image = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    fixed_number = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    max_number = serializers.IntegerField(
        required=False,
        allow_null=True,
    )
    is_unlimited = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    is_asset_anchored = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    anchor_asset_type = serializers.ChoiceField(
        required=False,
        allow_blank=True,
        allow_null=True,
        choices=ANCHOR_ASSET_TYPE_CHOICES,
    )
    anchor_asset = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    attestation_of_reserve = serializers.URLField(
        required=False, allow_blank=True, allow_null=True
    )
    redemption_instructions = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    collateral_addresses = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )
    collateral_address_messages = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )
    collateral_address_signatures = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )
    regulated = serializers.BooleanField(
        required=False,
        allow_null=True,
    )
    approval_server = serializers.URLField(
        required=False, allow_blank=True, allow_null=True
    )
    approval_criteria = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )


class GenerateTOMLSerializer(serializers.Serializer):
    general_info = TOMLGeneralInfo(required=False)
    org_doc = TOMLOrganizationDoc(required=False)
    point_of_contact_doc = TOMLPointOfContactDoc(required=False, many=True)
    currency_doc = TOMLCurrencyDoc(required=False, many=True)


class AccountOptionsSerializer(serializers.Serializer):
    clawback = serializers.BooleanField(required=True)
    freeze = serializers.BooleanField(required=True)
    signers = serializers.ListField(
        child=serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH),
        required=False,
        allow_null=True,
    )


class SetOptionsRequestSerializer(AccountOptionsSerializer):
    public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH, required=True)
