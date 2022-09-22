from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _


class GreaterThanValidator(BaseValidator):
    message = _("Ensure this value is greater than %(limit_value)s.")
    code = "min_value"

    def compare(self, a, b):
        return a <= b


def HTTPSValidator(value: str):
    if value and not value.startswith("https://"):
        raise ValidationError("Only URLs with HTTPS are allowed.")
