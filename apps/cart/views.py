from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product

from .models import Cart, CartItem

from .serializers import CartSerializer


class CartAPIView(generics.RetrieveAPIView):

    serializer_class = CartSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):

        return self.request.user.cart


class AddToCartAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        quantity = request.data.get("quantity", 1)

        product = Product.objects.get(id=product_id)

        cart = request.user.cart

        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:

            item.quantity += int(quantity)

        else:

            item.quantity = int(quantity)

        item.save()

        return Response({"message": "Товар добавлен в корзину"})


class RemoveCartItemAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        item = CartItem.objects.get(id=pk, cart=request.user.cart)

        item.delete()

        return Response({"message": "Удалено"})
