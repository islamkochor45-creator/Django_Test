from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        CUSTOMER = "customer", "Customer"

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email


from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    bio = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"Profile: {self.user.email}"
