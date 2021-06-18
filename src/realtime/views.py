from django.shortcuts import render

from accounts.models import RaspDevice, Car
from accounts.views import getNotifications
from .models import Drive, Alert

# Drives management page
def drives(request):
    company = request.user.profile.company
    drs = Drive.objects.filter(device__car__company=company).order_by('-endTime')
    
    lastestAlerts, unreadCounts = getNotifications(company)

    context = {'drs': drs, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "drives.html", context)

# Alerts management page
def alerts(request):
    company = request.user.profile.company
    lastestAlerts, unreadCounts = getNotifications(company)
    
    context = {'drs': lastestAlerts, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "alerts.html", context)


def driveDetail(request, id):
    drive = Drive.objects.get(id=id)
    alerts = drive.alert_set.all()[:1]
    
    for alert in alerts:
        alert.isRead = True
        alert.save()
    
    alerts = len(alerts)

    company = request.user.profile.company
    lastestAlerts = Alert.objects.filter(drive__device__car__company=company).order_by('-timeOccured')[:5]
    
    unreadCounts = 0
    for alert in lastestAlerts:
        unreadCounts = (unreadCounts + 1) if not alert.isRead else unreadCounts

    context = {"drive": drive, "alerts": alerts, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "driveDetail.html", context)


def carDrives(request, id):
    company = request.user.profile.company
    car = Car.objects.get(id=id)
    drives = Drive.objects.filter(device__car=car).order_by('-startTime')

    lastestAlerts, unreadCounts = getNotifications(company)
    context = {'drs': drives, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "car.html", context)