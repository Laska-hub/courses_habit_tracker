from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.validators import validate_habit

User = get_user_model()


class HabitTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123",
            telegram_chat_id="123456",
        )

        self.client.force_authenticate(
            user=self.user,
        )

    def test_create_habit(self):
        response = self.client.post(
            "/api/habits/",
            {
                "place": "Дом",
                "time": "08:00:00",
                "action": "Зарядка",
                "execution_time": 60,
                "period": 1,
                "is_public": False,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Habit.objects.count(),
            1,
        )

        habit = Habit.objects.first()

        self.assertEqual(
            habit.user,
            self.user,
        )

    def test_list_user_habits(self):
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            execution_time=60,
        )

        response = self.client.get(
            "/api/habits/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["results"]),
            1,
        )

    def test_update_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            execution_time=60,
        )

        response = self.client.patch(
            f"/api/habits/{habit.id}/",
            {
                "action": "Бег",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        habit.refresh_from_db()

        self.assertEqual(
            habit.action,
            "Бег",
        )

    def test_delete_habit(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00:00",
            action="Зарядка",
            execution_time=60,
        )

        response = self.client.delete(
            f"/api/habits/{habit.id}/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(Habit.objects.filter(id=habit.id).exists())

    def test_validator_reward_and_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00:00",
            action="Ванна",
            execution_time=60,
            is_pleasant=True,
        )

        with self.assertRaises(ValidationError):
            validate_habit(
                {
                    "reward": "Шоколад",
                    "related_habit": pleasant_habit,
                    "execution_time": 60,
                    "period": 1,
                }
            )

    def test_validator_execution_time(self):
        with self.assertRaises(ValidationError):
            validate_habit(
                {
                    "execution_time": 121,
                    "period": 1,
                }
            )

    def test_validator_related_habit_must_be_pleasant(self):
        bad_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="10:00:00",
            action="Работа",
            execution_time=60,
            is_pleasant=False,
        )

        with self.assertRaises(ValidationError):
            validate_habit(
                {
                    "related_habit": bad_habit,
                    "execution_time": 60,
                    "period": 1,
                }
            )

    def test_validator_pleasant_habit(self):
        with self.assertRaises(ValidationError):
            validate_habit(
                {
                    "is_pleasant": True,
                    "reward": "Кофе",
                    "execution_time": 60,
                    "period": 1,
                }
            )

    def test_validator_period(self):
        with self.assertRaises(ValidationError):
            validate_habit(
                {
                    "execution_time": 60,
                    "period": 8,
                }
            )
