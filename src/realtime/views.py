from django.shortcuts import render

from accounts.models import RaspDevice
from .models import Drive, Alert


def detail(request, id):
    pi = RaspDevice.objects.get(id=id)

    if pi.status == "offline":
        alerts = 0
    else:
        ongoingDrive = pi.drive_set.all().get(status="ongoing")
        alerts = len(ongoingDrive.alert_set.all())

    context = {"pi": pi, "alerts": alerts}
    return render(request, "detail.html", context)


# def detail(request, id):
#     drive = Drive.objects.get(id=id)
#     alerts = len(drive.alert_set.all())

#     context = {"drive": drive, "alerts": alerts}
#     return render(request, "detail.html", context)
