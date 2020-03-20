
import time
import hashlib
from django.db import models


def _create_hash():
    m = hashlib.sha1()
    m.update(str(time.time()).encode('utf-8'))
    return m.hexdigest()


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    hash = models.CharField(max_length=200, default=_create_hash, unique=True)

    def __str__(self):
        return self.nome


class Favorito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto_id = models.IntegerField()
    hash = models.CharField(max_length=200, default=_create_hash, unique=True)

    class Meta:
        unique_together = (('cliente', 'produto_id'),)

    def __str__(self):
        return f'{self.cliente.nome} - {self.produto_id}'
