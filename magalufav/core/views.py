
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Favorito, Cliente
from .serializers import FavoritoSerializer, ClienteSerializer


class ClientesViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Cliente.objects.all()
        serializer = ClienteSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Cliente.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ClienteSerializer(user)
        return Response(serializer.data)


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
