from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    email = models.EmailField(
        unique=True,
        verbose_name="email",
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name="first name",
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name="last name",
        blank=True,
    )

    telegram_chat_id = models.CharField(
        max_length=100,
        verbose_name="telegram chat id",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
