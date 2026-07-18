from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from apps.catalog.models import Product

from .models import Review

from .serializers import ReviewSerializer


class ProductReviewsAPIView(APIView):

    def get(self, request, product_id):

        reviews = Review.objects.filter(product_id=product_id)

        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)


class CreateReviewAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get("product_id")

        product = Product.objects.get(id=product_id)

        review = Review.objects.create(
            user=request.user,
            product=product,
            rating=request.data.get("rating"),
            text=request.data.get("text"),
        )

        serializer = ReviewSerializer(review)

        return Response(serializer.data)
