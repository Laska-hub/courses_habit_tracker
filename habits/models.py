from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
    )

    place = models.CharField(
        max_length=255,
    )

    time = models.TimeField()

    action = models.CharField(
        max_length=255,
    )

    is_pleasant = models.BooleanField(
        default=False,
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_habits",
    )

    period = models.PositiveIntegerField(
        default=1,
        help_text="Periodicity in days",
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    execution_time = models.PositiveIntegerField(
        help_text="Execution time in seconds",
    )

    is_public = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.action
