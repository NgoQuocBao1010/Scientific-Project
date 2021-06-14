from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from realtime import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("drive/", include("realtime.urls")),
    path("alerts/", views.alerts, name="alerts"),
    path("car/<str:id>/", views.carDrives, name="carDrives"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)