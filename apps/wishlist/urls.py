from django.urls import path

from .views import WishlistAPIView, AddWishlistAPIView, RemoveWishlistAPIView

urlpatterns = [
    path("", WishlistAPIView.as_view()),
    path("add/", AddWishlistAPIView.as_view()),
    path("remove/<int:pk>/", RemoveWishlistAPIView.as_view()),
]
