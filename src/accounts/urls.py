from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("home/", views.home, name="home"),
    path("account-setting/", views.accountSettings, name="accountSettings"),
    path(
        "logout/",
        views.logoutUser,
        name="logout",
    ),
    path('removeCar/<str:id>/', views.removeCar, name='removeCar'),
]