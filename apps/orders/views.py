from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from .models import Order

from .serializers import OrderSerializer


class CreateOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = request.user.cart

        if not cart.items.exists():

            return Response({"error": "Корзина пустая"}, status=400)

        order = Order.objects.create(
            user=request.user,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            phone=request.data.get("phone"),
            address=request.data.get("address"),
        )

        for item in cart.items.all():

            order.items.create(
                product=item.product, quantity=item.quantity, price=item.product.price
            )

        cart.items.all().delete()

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class MyOrdersAPIView(generics.ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(user=self.request.user)


class UpdateOrderStatusAPIView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        order = Order.objects.get(id=pk)

        status = request.data.get("status")

        order.status = status

        order.save()

        return Response({"message": "Статус изменен", "status": order.status})


class OrderDetailAPIView(generics.RetrieveAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(user=self.request.user)


class AdminOrdersAPIView(generics.ListAPIView):

    serializer_class = OrderSerializer

    permission_classes = [IsAdminUser]

    queryset = Order.objects.all()
