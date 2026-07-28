from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:

        model = Review

        fields = [
            "id",
            "user",
            "rating",
            "text",
            "created_at",
        ]


class CreateReviewSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField(required=False, allow_blank=True)
