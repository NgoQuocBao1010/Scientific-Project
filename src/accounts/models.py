from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name="name"),
            models.UniqueConstraint(fields=["roomCode"], name="roomCode"),
        ]

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)
    roomCode = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return "Company " + self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    dateCreated = models.DateTimeField(auto_now_add=True)
    profilePic = models.ImageField(default="huongtram.png", null=True, blank=True)

    def __str__(self):
        return self.name + " profile"


class Car(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["licensePlate"], name="licensePlate"),
        ]

    name = models.CharField(max_length=50)
    licensePlate = models.CharField(max_length=20, null=True)
    boughtDate = models.DateTimeField(auto_now_add=True, null=True)
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class RaspDevice(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["password"], name="password"),
        ]
    
    STATUS = (
        ("online", "online"),
        ("offline", "offline"),
    )
    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.SET_NULL, blank=True)
    status = models.CharField(
        max_length=50, null=True, blank=True, choices=STATUS, default="offline"
    )
    password = models.CharField(max_length=8, null=True, blank=True)
    dateAdded = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} from {self.company}'