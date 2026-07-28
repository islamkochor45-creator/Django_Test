from django.urls import path

from .views import ProductReviewsAPIView, CreateReviewAPIView

urlpatterns = [
    path("product/<int:product_id>/", CreateReviewAPIView.as_view()),
    path("create/", ProductReviewsAPIView.as_view()),
]
