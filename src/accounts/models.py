from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLES = (
        ("admin", "admin"),
        ("driver", "driver"),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES)
    email = models.CharField(max_length=30, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    # profilePic = models.ImageField(default='football.jpg', null=True, blank=True)

    def __str__(self):
        return self.name + " profiles"


class Driver(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    licenseDriver = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "Driver " + self.profile.name


class Car(models.Model):
    name = models.CharField(max_length=50)
    driver = models.ForeignKey(Driver, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RaspDevice(models.Model):
    STATUS = (
        ("online", "online"),
        ("offline", "offline"),
    )
    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    lastActive = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
