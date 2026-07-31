from django.urls import path

from rest_framework.routers import DefaultRouter

from habits.views import (
    HabitViewSet,
    PublicHabitListAPIView,
)


router = DefaultRouter()

router.register(
    "habits",
    HabitViewSet,
    basename="habits",
)

urlpatterns = [
    path(
        "public/",
        PublicHabitListAPIView.as_view(),
        name="public-habits",
    ),
]

urlpatterns += router.urls
