from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, RegisterView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
# router.register(r"create_user", RegisterView, basename="create_user")

urlpatterns = [
    path("tasks/", include(router.urls)),
    path("create_users/", include("urls.py")),
]
