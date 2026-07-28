from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = [
            "id",
            "order",
            "amount",
            "method",
            "status",
            "transaction_id",
            "created_at",
        ]


class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    method = serializers.ChoiceField(
        choices=["card", "cash"],  # замени на реальные варианты из модели Payment
        default="card",
        required=False,
    )
