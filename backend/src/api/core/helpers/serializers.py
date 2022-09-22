from collections import OrderedDict

from rest_framework import serializers


class NonEmptySerializer(serializers.Serializer):
    def validate(self, data):
        return OrderedDict({k: v for k, v in data.items() if v not in [None, "", []]})
