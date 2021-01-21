from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('activityLog/<str:pk>/', views.activityLog, name='activityLog'),
]