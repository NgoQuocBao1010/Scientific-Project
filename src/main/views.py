from django.shortcuts import render

from .models import *


def home(request):
    piDevices = RaspberryDevice.objects.all()

    piNames = list(map(lambda x: x.name, piDevices))

    context = {
        'devicesName': piNames,
        'devices': piDevices,
    }

    return render(request, 'main/home.html', context)


def activityLog(request, pk):
    piDevice = RaspberryDevice.objects.get(id=pk)
    lastestActivity = piDevice.activity_set.all().order_by('timeOccured')

    context = {
        'device': piDevice,
        'activity': lastestActivity,
    }

    return render(request, 'main/activity.html', context)
