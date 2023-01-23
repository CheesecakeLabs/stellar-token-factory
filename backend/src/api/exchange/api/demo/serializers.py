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


class BalanceSerializer(serializers.Serializer):
    balance = serializers.CharField()
    asset_code = serializers.CharField(max_length=STELLAR_CODE_MAX_LENGTH)
    asset_issuer = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
