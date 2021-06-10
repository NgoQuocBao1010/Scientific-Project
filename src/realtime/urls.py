from django.urls import path
from . import views

urlpatterns = [
    path("", views.drives, name="drives"),
    path("<str:id>", views.driveDetail, name="driveDetail"),
]