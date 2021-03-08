from django.shortcuts import render

from accounts.models import RaspDevice


def activityPage(request):
    devices = RaspDevice.objects.all()
    onlineDevices = RaspDevice.objects.filter(status="online")

    context = {
        "devices": devices,
        "onlDevices": onlineDevices,
    }
    return render(request, "activity.html", context)
