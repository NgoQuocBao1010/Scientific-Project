from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "Company " + self.name


class Profile(models.Model):
    ROLES = (
        ("admin", "admin"),
        ("driver", "driver"),
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=30, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLES)
    dateCreated = models.DateTimeField(auto_now_add=True)
    profilePic = models.ImageField(default="huongtram.png", null=True, blank=True)

    def __str__(self):
        return self.name + " profile"


class Driver(models.Model):
    profile = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    licenseDriver = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "Driver " + self.profile.name


class Car(models.Model):
    name = models.CharField(max_length=50)
    licensePlate = models.CharField(max_length=20, null=True)
    boughtDate = models.DateTimeField(auto_now_add=True, null=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RaspDevice(models.Model):
    STATUS = (
        ("online", "online"),
        ("offline", "offline"),
    )
    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS, default="offline")
    ipaddress = models.CharField(max_length=50, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name