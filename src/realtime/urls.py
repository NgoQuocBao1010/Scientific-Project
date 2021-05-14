from django.urls import path
from . import views

urlpatterns = [
    path("<str:id>", views.driveDetail, name="driveDetail"),
]