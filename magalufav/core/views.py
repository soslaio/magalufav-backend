
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Favorito, Cliente
from .serializers import FavoritoSerializer, ClienteSerializer


class ClientesViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        cliente = get_object_or_404(Cliente, hash=pk)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = ClienteSerializer(data=request.data)
            validacao = serializer.is_valid(raise_exception=True)

            return Response(status=201, data={'id': validacao})
        except Exception as err:
            errors = [dict(field=k, errors=v) for k, v in err.detail.items()]
            return Response(status=400, data=dict(errors=errors))

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class FavoritosViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Favorito.objects.all()
        serializer = FavoritoSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Favorito.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = FavoritoSerializer(user)
        return Response(serializer.data)
