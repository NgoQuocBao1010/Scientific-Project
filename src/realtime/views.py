from django.shortcuts import render

from .models import Drive
from accounts.models import RaspDevice


def drivesMangementPage(request):
    devices = RaspDevice.objects.all()
    onlineDevices = RaspDevice.objects.filter(status="online")

    context = {
        "devices": devices,
        "onlDevices": onlineDevices,
    }
    return render(request, "drives.html", context)


def drivesOfPi(request, id):
    piDevice = RaspDevice.objects.get(id=id)

    previousDrives = (
        piDevice.drive_set.all().filter(status="ended").order_by("-startTime")
    )

    onDrive = (
        piDevice.drive_set.all().get(status="ongoing")
        if piDevice.status == "online"
        else None
    )

    context = {"pi": piDevice, "previousDrives": previousDrives, "onDrive": onDrive}
    return render(request, "drivesOfPi.html", context)