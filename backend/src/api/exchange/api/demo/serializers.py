from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

STELLAR_KEY_MAX_LENGTH = 56
STELLAR_CODE_MAX_LENGTH = 12


class PayeeSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    bank_account = serializers.CharField()
    stellar_wallet = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)


class PathPaymentStrictReceiveRequestSerializer(serializers.Serializer):
    destination_public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    receive_amount = serializers.FloatField()
    user_id = serializers.CharField()


class PathPaymentStrictReceiveResponseSerializer(serializers.Serializer):
    envelope_xdr = serializers.CharField()
    final_cost = serializers.FloatField()
    required_signatures = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_null=True,
    )


class BalanceSerializer(serializers.Serializer):
    balance = serializers.FloatField()
    asset_code = serializers.CharField(max_length=STELLAR_CODE_MAX_LENGTH)
    asset_issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
