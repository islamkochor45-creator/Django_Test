from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.catalog.models import Product

from .models import WishlistItem
from .serializers import WishlistSerializer


class WishlistAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        wishlist = request.user.wishlist

        serializer = WishlistSerializer(wishlist)

        return Response(serializer.data)


class AddWishlistAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        product = Product.objects.get(id=product_id)

        WishlistItem.objects.get_or_create(
            wishlist=request.user.wishlist, product=product
        )

        return Response({"message": "Добавлено в избранное"})


class RemoveWishlistAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        item = WishlistItem.objects.get(id=pk, wishlist=request.user.wishlist)

        item.delete()

        return Response({"message": "Удалено"})
