from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, RegisterView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"users", RegisterView, basename="user")

urlpatterns = [
    path("tasks/", include(router.urls)),
    path("create_users", include(router.urls)),
]
