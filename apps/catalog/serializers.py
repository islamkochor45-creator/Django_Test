from apps.catalog.models import Product, Category, ProductImage
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "is_active",
        ]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage

        fields = [
            "id",
            "image",
            "is_main",
        ]


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)

    average_rating = serializers.ReadOnlyField()

    class Meta:

        model = Product

        fields = [
            "id",
            "category_id",
            "category",
            "name",
            "slug",
            "description",
            "sku",
            "price",
            "quantity",
            "brand",
            "status",
            "is_active",
            "images",
            "average_rating",
        ]
