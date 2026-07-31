from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class HabitViewSet(viewsets.ModelViewSet):
    """
    API для работы с привычками.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = HabitPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()

        return Habit.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

class PublicHabitListAPIView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    queryset = Habit.objects.filter(is_public=True)
