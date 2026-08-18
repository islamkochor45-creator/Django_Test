from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Order, OrderChatMessage, OrderChatThread

from .serializers import OrderChatThreadSerializer, OrderSerializer


class IsManagerOrAdmin(BasePermission):
    message = "Только менеджер или администратор может обновлять статус заказа."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in {"manager", "admin"} or request.user.is_staff or request.user.is_superuser


@extend_schema(
    request=OrderSerializer,
    responses={200: None},
)
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

    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def patch(self, request, pk):

        order = Order.objects.get(id=pk)

        status = request.data.get("status")

        if status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Некорректный статус"}, status=400)

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

    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    queryset = Order.objects.all()


class OrderChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        message_text = request.data.get("message", "").strip()

        if not order_id:
            return Response({"error": "order_id обязателен"}, status=400)
        if not message_text:
            return Response({"error": "message обязателен"}, status=400)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Заказ не найден"}, status=404)

        if request.user != order.user and request.user.role not in {"manager", "admin"}:
            return Response({"error": "Нет прав для общения по этому заказу"}, status=403)

        thread, _ = OrderChatThread.objects.get_or_create(order=order)
        message = OrderChatMessage.objects.create(
            thread=thread,
            sender=request.user,
            content=message_text,
        )

        return Response(
            {
                "thread": thread.id,
                "message": message.content,
                "sender": request.user.email,
                "created_at": message.created_at,
            }
        )

    def get(self, request):
        threads = OrderChatThread.objects.filter(order__user=request.user)
        if request.user.role in {"manager", "admin"}:
            threads = OrderChatThread.objects.all()

        serializer = OrderChatThreadSerializer(threads, many=True)
        return Response(serializer.data)
