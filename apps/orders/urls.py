from django.urls import path

from .views import (
    CreateOrderAPIView,
    MyOrdersAPIView,
    OrderDetailAPIView,
    AdminOrdersAPIView,
    UpdateOrderStatusAPIView,
)

urlpatterns = [
    path("", MyOrdersAPIView.as_view()),
    path("create/", CreateOrderAPIView.as_view()),
    path("<int:pk>/", OrderDetailAPIView.as_view()),
    path("admin/all/", AdminOrdersAPIView.as_view()),
    path("admin/status/<int:pk>/", UpdateOrderStatusAPIView.as_view()),
]
