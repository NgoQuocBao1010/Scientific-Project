from django.shortcuts import render

from accounts.models import RaspDevice


def detail(request, id):
    pi = RaspDevice.objects.get(id=id)

    if pi.status == "offline":
        alerts = 0
    else:
        ongoingDrive = pi.drive_set.all().get(status="ongoing")
        alerts = len(ongoingDrive.alert_set.all())

    context = {"pi": pi, "alerts": alerts}
    return render(request, "detail.html", context)
