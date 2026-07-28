from rest_framework import serializers

from apps.catalog.serializers import ProductSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    total_price = serializers.ReadOnlyField()

    class Meta:

        model = CartItem

        fields = [
            "id",
            "product",
            "quantity",
            "total_price",
        ]


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True, read_only=True)

    total_price = serializers.ReadOnlyField()

    class Meta:

        model = Cart

        fields = [
            "id",
            "items",
            "total_price",
        ]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)
