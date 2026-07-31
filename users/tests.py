from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserTests(APITestCase):

    def test_register_user(self):
        response = self.client.post(
            "/api/users/register/",
            {
                "email": "user@example.com",
                "password": "password123",
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="user@example.com",
            ).exists()
        )

    def test_profile_authenticated(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="password123",
        )

        self.client.force_authenticate(
            user=user,
        )

        response = self.client.get(
            "/api/users/profile/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            user.email,
        )

    def test_update_profile(self):
        user = User.objects.create_user(
            email="user@example.com",
            password="password123",
        )

        self.client.force_authenticate(
            user=user,
        )

        response = self.client.patch(
            "/api/users/profile/",
            {
                "first_name": "Alice",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        user.refresh_from_db()

        self.assertEqual(
            user.first_name,
            "Alice",
        )

    def test_profile_requires_auth(self):
        response = self.client.get(
            "/api/users/profile/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_user_manager(self):
        user = User.objects.create_user(
            email="manager@test.com",
            password="password123",
        )

        self.assertEqual(
            user.email,
            "manager@test.com",
        )

        self.assertTrue(
            user.check_password(
                "password123",
            )
        )

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="password123",
            )

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@test.com",
            password="password123",
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
