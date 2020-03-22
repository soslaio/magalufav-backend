
from rest_framework import serializers
from .models import Favorite, Customer


class FavoriteWithProductsSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    image = serializers.URLField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    link = serializers.URLField()
    reviewScore = serializers.DecimalField(max_digits=10, decimal_places=6)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
