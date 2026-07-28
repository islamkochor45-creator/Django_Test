from django.urls import path

from .views import ProductReviewsAPIView, CreateReviewAPIView

urlpatterns = [
    path("create/", CreateReviewAPIView.as_view()),
    path("product/<int:product_id>/", ProductReviewsAPIView.as_view()),
]
