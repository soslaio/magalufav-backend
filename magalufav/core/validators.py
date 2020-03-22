
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

from .api import request_product_details


def check_product_existence(value):
    status_code, _ = request_product_details(value)
    if status_code != 200:
        raise ValidationError('O produto não existe', code='invalid')
