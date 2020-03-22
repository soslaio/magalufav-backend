
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorito, Cliente
from .serializers import FavoritoSerializer, ClienteSerializer

# from rest_framework.pagination import PageNumberPagination


# TODO: verificar os cabeçalhos de respostas utilizado nas apis
class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=True, methods=['GET'])
    def favorites(self, request, pk=None):
        favorites = Favorito.objects.filter(cliente_id=pk)

        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = FavoritoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FavoritoSerializer(favorites, many=True)
        return Response(status=200, data={'favorites': serializer.data})


# TODO: Incluir paginação na lista de favoritos
class FavoritosViewSet(viewsets.ModelViewSet):
    queryset = Favorito.objects.all()
    serializer_class = FavoritoSerializer
