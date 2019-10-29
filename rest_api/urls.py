from django.urls import path

from rest_api.views import Register, Login, Logout, UserProfile

urlpatterns = [
    path(
        route="rest_api/register",
        view=Register.as_view(),
        name="register"
    ),

    path(
        route="rest_api/login",
        view=Login.as_view(),
        name="login"
    ),

    path(
        route="rest_api/logout",
        view=Logout.as_view(),
        name="logout"
    ),

    path(
        route="rest_api/user/",
        view=UserProfile.as_view(),
        name="user_void"
    ),

    path(
        route="rest_api/user/<str:username>",
        view=UserProfile.as_view(),
        name="user"
    ),
]