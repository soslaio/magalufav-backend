
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Favorito, Cliente
from .serializers import FavoritoSerializer, ClienteSerializer
from rest_framework import mixins


class CustomViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    Modificação do ModelViewSet para desabilitar o método de listagem.
    """
    pass


class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


# TODO: Incluir paginação na lista de favoritos
class FavoritosViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
