from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("home/", views.home, name="home"),
    path(
        "logout/",
        views.logoutUser,
        name="logout",
    ),
]