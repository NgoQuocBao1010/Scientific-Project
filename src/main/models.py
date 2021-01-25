from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class RaspberryDevice(models.Model):
    STATUS = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    )

    name = models.CharField(max_length=50)
    car = models.OneToOneField(Car, null=True, on_delete=models.CASCADE)
    status = models.CharField(default='Offline', max_length=20, choices=STATUS)
    lastActive = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} (pi devices from {self.car})'


class Activity(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['timeOccured'], name='time'),
        ]

    STATUS = (
        ('Starting', 'Starting'),
        ('Stopped', 'Stopped'),
        ('Yawning', 'Yawning'),
        ('Drowsiness', 'Drowsiness'),
        ('Unconscious', 'Unconscious'),
    )

    devices = models.ForeignKey(RaspberryDevice,
                                null=True,
                                on_delete=models.CASCADE)
    activityName = models.CharField(max_length=50, choices=STATUS)
    timeOccured = models.DateTimeField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    isRead = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.devices.name} - {self.activityName} at {self.timeOccured}'
