from django.urls import path

from . import views

urlpatterns = [
    path("", views.drivesMangementPage, name="drives"),
    path("drives_of_pi/<str:id>/", views.drivesOfPi, name="drivesOfPi"),
    path("evidence/", views.drivesOfPi, name="image"),
]
