from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated


from rest_framework import viewsets

from apps.users.models import User

# from .serializers import UserSerializer
# from .tasks import send_email_task

# Create your views here.
from .serializers import RegisterSerializer
from .tasks import send_email_task


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def perform_create(self, serializer):
        user = User.objects.create_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        send_email_task.delay(user.email)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        send_email_task.delay(user.email)
