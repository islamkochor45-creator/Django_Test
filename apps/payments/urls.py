from django.urls import path

from .views import CreatePaymentAPIView, ConfirmPaymentAPIView

urlpatterns = [
    path("create/", CreatePaymentAPIView.as_view()),
    path("confirm/<int:pk>/", ConfirmPaymentAPIView.as_view()),
]
