from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Authentication
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    # Users
    path("users/", views.userPage, name="users"),
    path("addUser/", views.addUserPage, name="addUser"),
    path("driverInfo/<str:id>/", views.driverInfo, name="driverInfo"),
    # Profile
    path("profile/<str:id>/", views.profilePage, name="profile"),
    path("editProfile/<str:id>/", views.editProfile, name="editProfile"),
    path("deleteUser/<str:id>/", views.delUserPage, name="deleteUser"),
    # Password Reset
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]