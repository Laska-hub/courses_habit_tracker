from django.urls import path

from users.views import (
    RegisterView,
    UserProfileView,
)


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "profile/",
        UserProfileView.as_view(),
        name="profile",
    ),
]
