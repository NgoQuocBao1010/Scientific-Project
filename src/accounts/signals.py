from django.db.models.signals import post_save, pre_delete

from .models import Car
from .customPrint import MyCustomPrint

def removeAllDrives(sender, instance, **kwargs):
    """ Remove all the drive instance related to a car after its deleted """
    try:
        rasp = instance.raspdevice
        rasp.drive_set.all().delete()
    except Exception as e:
        MyCustomPrint(f"Error deleting its drives", style="error")
    finally:
        MyCustomPrint(f"Car {instance} from {instance.company} and all its drives are deleted", style="success")


pre_delete.connect(removeAllDrives, sender=Car)