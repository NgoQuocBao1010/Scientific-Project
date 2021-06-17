from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from .models import RaspDevice, Car

def raspConfig(sender, instance, created, **kwargs):
    if created:
        print(instance)
        print(kwargs)
        # RaspDevice.objects.create(
            
        # )
        print('Rasp added!!')

# post_save.connect(raspConfig, sender=Car)