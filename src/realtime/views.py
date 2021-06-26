from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from accounts.models import RaspDevice, Car
from accounts.views import getNotifications
from .models import Drive, Alert

# Drives management page
@login_required(login_url="/")
def drives(request):
    company = request.user.profile.company
    drs = Drive.objects.filter(device__company=company).order_by('-startTime')

    # Search filter
    searchKey = request.GET.get("search-key")

    if searchKey != '' and searchKey is not None:
        drs = drs.filter(device__car__licensePlate__icontains=searchKey)
    
    lastestAlerts, unreadCounts = getNotifications(company)

    context = {'drs': drs, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "drives.html", context)

# Alerts management page
@login_required(login_url="/")
def alerts(request):
    company = request.user.profile.company
    drs = Drive.objects.filter(device__company=company, alert__gt=0).order_by('-startTime').annotate(total=Count('id'))
    

    # Search filter
    searchKey = request.GET.get("search-key")

    if searchKey != '' and searchKey is not None:
        drs = drs.filter(device__car__licensePlate__icontains=searchKey)
    
    lastestAlerts, unreadCounts = getNotifications(company)
    
    context = {'drs': drs, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "alerts.html", context)


# Detail of an specific drive (start, end, alerts ...) 
@login_required(login_url="/")
def driveDetail(request, id):
    company = request.user.profile.company
    drive = Drive.objects.get(id=id)

    if drive.device.car.company != company:
        return HttpResponse('<h1>You are not authorized to view this page</h1>')

    alerts = drive.alert_set.all()
    
    for alert in alerts:
        alert.isRead = True
        alert.save()
    
    alerts = len(alerts)

    lastestAlerts, unreadCounts = getNotifications(company)

    context = {"drive": drive, "alerts": alerts, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "driveDetail.html", context)


# Return every drives of individual car
@login_required(login_url="/")
def carDrives(request, id):
    company = request.user.profile.company
    car = Car.objects.get(id=id)

    if car.company != company:
        return HttpResponse('<h1>You are not authorized to view this page</h1>')
    
    drives = Drive.objects.filter(device__car=car).order_by('-startTime')

    lastestAlerts, unreadCounts = getNotifications(company)
    context = {
        'drs': drives, 
        'car': car, 
        "notifications": lastestAlerts, 
        "unreadNotis": unreadCounts
    }
    return render(request, "car.html", context)