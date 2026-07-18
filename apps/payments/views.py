from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order

from .models import Payment

from .serializers import PaymentSerializer


class CreatePaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get("order_id")

        order = Order.objects.get(id=order_id, user=request.user)

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "amount": order.total_price,
                "method": request.data.get("method", "card"),
            },
        )

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)


class ConfirmPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        payment = Payment.objects.get(id=pk, order__user=request.user)

        payment.status = "paid"

        payment.transaction_id = "TEST_TRANSACTION_123"

        payment.save()

        payment.order.status = "processing"

        payment.order.save()

        return Response({"message": "Оплата успешна"})
