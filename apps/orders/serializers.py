from rest_framework import serializers

from .models import Order, OrderChatMessage, OrderChatThread, OrderItem

from apps.catalog.serializers import ProductSerializer


class OrderChatMessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = OrderChatMessage
        fields = ["id", "sender", "sender_email", "content", "created_at"]

    def get_sender_email(self, obj):
        return obj.sender.email


class OrderChatThreadSerializer(serializers.ModelSerializer):
    messages = OrderChatMessageSerializer(many=True, read_only=True)
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = OrderChatThread
        fields = ["id", "order_id", "messages", "created_at", "updated_at"]


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
