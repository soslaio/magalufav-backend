
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Favorite, Customer
from .serializers import FavoritoSerializer, ClienteSerializer


# TODO: verificar os cabeçalhos de respostas utilizado nas apis
class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = ClienteSerializer

    @action(detail=True, methods=['GET'])
    def favorites(self, request, pk=None):
        favorites = Favorite.objects.filter(customer_id=pk)

        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = FavoritoSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FavoritoSerializer(favorites, many=True)
        return Response(status=200, data={'favorites': serializer.data})


class FavoritosViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoritoSerializer
