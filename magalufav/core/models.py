
import uuid
from django.db import models

from .validators import check_product_existence


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=200, validators=[check_product_existence])

    class Meta:
        ordering = ['customer']
        unique_together = (('customer', 'product_id'),)

    @property
    def url(self):
        return f'http://challenge-api.luizalabs.com/api/product/{self.product_id}'

    def __str__(self):
        return f'{self.customer.name} - {self.product_id}'
