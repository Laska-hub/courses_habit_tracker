from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "telegram_chat_id",
        )
        read_only_fields = (
            "id",
        )


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "telegram_chat_id",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )

        return user
