from django.shortcuts import render

from .models import *


def home(request):
    piDevices = RaspberryDevice.objects.all()

    piNames = list(map(lambda x: x.name, piDevices))
    onlDevices = piDevices.filter(status='Online')

    context = {
        'devices': piNames,
        'onlDevices': onlDevices,
    }

    return render(request, 'main/home.html', context)
