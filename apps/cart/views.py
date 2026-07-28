from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.cart


@extend_schema(
    request=CartItemSerializer,
    responses={200: None},
)
class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        if not product_id:
            return Response(
                {"error": "Поле product_id обязательно"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response(
                {"error": "quantity должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Товар с таким id не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart = request.user.cart

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"message": "Товар добавлен в корзину"})


class RemoveCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            item = CartItem.objects.get(id=pk, cart=request.user.cart)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Элемент корзины не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        item.delete()

        return Response({"message": "Удалено"})
