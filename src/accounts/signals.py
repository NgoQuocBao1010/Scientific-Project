from django.db.models.signals import post_save, pre_delete

from .models import Car

def removeAllDrives(sender, instance, **kwargs):
    try:
        rasp = instance.raspdevice
        rasp.drive_set.all().delete()

        print(f"[SERVER] Car {instance} from {instance.company} and all its drives are deleted\n")
    except Exception as e:
        print(f"[SERVER] Car {instance} from {instance.company} and all its drives are deleted\n")


pre_delete.connect(removeAllDrives, sender=Car)