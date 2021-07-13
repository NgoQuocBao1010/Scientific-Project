from django.db.models.signals import pre_delete

from .models import Car

def removeAllDrives(sender, instance, **kwargs):
    rasp = instance.raspdevice
    drives = rasp.drive_set.all().delete()

    print(f"\n[SERVER] Car {instance} and all its drives are deleted\n")

pre_delete.connect(removeAllDrives, sender=Car)