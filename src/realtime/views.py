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


def driveDetail(request, id):
    drive = Drive.objects.get(id=id)
    alerts = drive.alert_set.all()[:1]
    print(alerts)
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
