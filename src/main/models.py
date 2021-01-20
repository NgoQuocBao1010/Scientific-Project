from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True, blank=True)


class RaspberryDevice(models.Model):
    ipAdress = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.CASCADE)


class Activity(models.Model):
    STATUS = (
        ('Starting', 'Starting'),
        ('Offline', 'Offline'),
        ('Yawning', 'Yawning'),
        ('Drowsiness', 'Drowsiness'),
        ('Unconscious', 'Unconscious'),
    )

    devices = models.ForeignKey(RaspberryDevice,
                                null=True,
                                on_delete=models.CASCADE)
    activityName = models.CharField(max_length=50, choices=STATUS)
    timeOccured = models.DateTimeField(auto_now_add=True, null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
