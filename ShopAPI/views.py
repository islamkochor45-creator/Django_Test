from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


from rest_framework import viewsets

from apps.users.models import User

# from .serializers import UserSerializer
# from .tasks import send_email_task

# Create your views here.
from .serializers import RegisterSerializer
from .tasks import send_email_task


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # Создание пользователя
        # User.objects.create_user(...)

        # Отправка email через Celery
        send_email_task.delay(email)

        return Response(
            {"message": "Пользователь создан. Письмо отправлено в очередь."},
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        send_email_task.delay(user.email)
