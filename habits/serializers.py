from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = (
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "period",
            "reward",
            "execution_time",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        validate_habit(data)
        return data
