
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .api import fill_favorites
from .models import Favorite, Customer
from .serializers import FavoriteSerializer, CustomerSerializer, FavoriteWithProductsSerializer


# TODO: verificar os cabeçalhos de respostas utilizado nas apis
class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['GET'])
    def favorites(self, request, pk=None):

        # consulta os favoritos no banco e os preenche com
        # os dados do produto diretamente da api ou do cache
        favorites = Favorite.objects.filter(customer_id=pk)
        favorites_with_products = fill_favorites(favorites)

        # caso necessário, fatia o resultado em páginas
        page = self.paginate_queryset(favorites_with_products)
        if page is not None:
            serializer = FavoriteWithProductsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # caso não haja paginação, retorna a lista inteira
        serializer = FavoriteWithProductsSerializer(favorites_with_products, many=True)
        return Response(status=200, data={'favorites': serializer.data})


class FavoritosViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
