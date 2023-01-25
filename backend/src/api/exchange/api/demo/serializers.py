from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

STELLAR_KEY_MAX_LENGTH = 56


class PayeeSerializer(serializers.Serializer):
    name = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    bank_account = serializers.CharField()
    stellar_wallet = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)


class PathPaymentStrictReceiveResponseSerializer(serializers.Serializer):
    envelope_xdr = serializers.CharField()
    final_cost = serializers.FloatField()


class PathPaymentStrictReceiveRequestSerializer(serializers.Serializer):
    destination_public_key = serializers.CharField(max_length=STELLAR_KEY_MAX_LENGTH)
    receive_amount = serializers.FloatField()
