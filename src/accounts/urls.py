from django.urls import path
from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("home/", views.home, name="home"),
    path("driver/", views.driver, name="driver"),
    path(
        "logout/",
        views.logoutUser,
        name="logout",
    ),
    path('removeCar/<str:id>/', views.removeCar, name='removeCar'),
]