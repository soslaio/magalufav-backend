
from rest_framework import serializers
from .models import Favorite, Customer


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    image = serializers.URLField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.URLField()
    reviewScore = serializers.DecimalField(max_digits=2, decimal_places=6)


class FavoritoSerializer(serializers.ModelSerializer):
    # favorites = ProductSerializer(many=True,)

    class Meta:
        model = Favorite
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
