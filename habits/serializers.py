from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        validate_habit(data)
        return data
