from django.urls import path

from .views import CartAPIView, AddToCartAPIView, RemoveCartItemAPIView

urlpatterns = [
    path("", CartAPIView.as_view()),
    path("add/", AddToCartAPIView.as_view()),
    path("item/<int:pk>/", RemoveCartItemAPIView.as_view()),
]
