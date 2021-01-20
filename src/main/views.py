from django.shortcuts import render

from .models import *


def home(request):
    piDevices = RaspberryDevice.objects.all()

    onlDevices = piDevices.filter(status='Online')
    offDevices = piDevices.filter(status='Offline')

    context = {
        'offDevices': offDevices,
        'onlDevices': onlDevices,
    }

    return render(request, 'main/home.html', context)
