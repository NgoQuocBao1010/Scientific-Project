from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True, blank=True)


class Status(models.Model):
    STATUS_NAME = (
        ('Starting', 'Starting'),
        ('Offline', 'Offline'),
        ('Yawning', 'Yawning'),
        ('Drowsiness', 'Drowsiness'),
        ('Unconscious', 'Unconscious'),
    )

    name = models.CharField(max_length=50, choices=STATUS_NAME)
    description = models.CharField(max_length=50, null=True, blank=True)


class Activity(models.Model):
    pass


class RaspberryDevice(models.Model):
    ipAdress = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.CASCADE)
