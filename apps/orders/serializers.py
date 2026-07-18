from rest_framework import serializers

from .models import Order, OrderItem

from apps.catalog.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    total_price = serializers.ReadOnlyField()

    class Meta:

        model = OrderItem

        fields = [
            "id",
            "product",
            "quantity",
            "price",
            "total_price",
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)

    total_price = serializers.ReadOnlyField()

    class Meta:

        model = Order

        fields = [
            "id",
            "status",
            "payment_status",
            "first_name",
            "last_name",
            "phone",
            "address",
            "items",
            "total_price",
            "created_at",
        ]
