
from django.core.exceptions import ValidationError

from .api import request_product_details


# TODO: suporte para i18n
def check_product_existence(value):
    status_code, _ = request_product_details(value)
    if status_code != 200:
        raise ValidationError('O produto não existe.', code='invalid')
