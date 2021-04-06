from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from accounts.models import RaspDevice
from .models import ActiveCheck


def updateActive(sender, instance, created, **kwargs):
    if created:
        print()
        print(instance.date_created)
        print()
        if instance.status == "online":
            print(f"{instance} changed")
        else:
            print(f"{instance} created")


post_save.connect(updateActive, sender=RaspDevice)