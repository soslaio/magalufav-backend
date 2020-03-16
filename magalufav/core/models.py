
from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome


class Favorito(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto_id = models.IntegerField()

    class Meta:
        unique_together = (('cliente', 'produto_id'),)

    def __str__(self):
        return f'{self.cliente.nome} - {self.produto_id}'
