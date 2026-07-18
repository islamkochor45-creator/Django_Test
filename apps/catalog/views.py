from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Product
from .filters import ProductFilter
from .serializers import CategorySerializer, ProductSerializer


class CategoryListAPIView(generics.ListCreateAPIView):

    queryset = Category.objects.all()

    serializer_class = CategorySerializer


class ProductListAPIView(generics.ListCreateAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    # filterset_fields = [
    #     "category",
    #     "status",
    #     "brand",
    # ]
    filterset_class = ProductFilter

    search_fields = [
        "name",
        "description",
        "brand",
        "sku",
    ]

    ordering_fields = [
        "price",
        "created_at",
        "quantity",
    ]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer
