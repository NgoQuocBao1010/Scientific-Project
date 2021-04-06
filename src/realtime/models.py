from django.db import models

from accounts.models import RaspDevice


class Activity(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["timeOccured"], name="time"),
        ]

    STATUS = (
        ("Starting", "Starting"),
        ("Stopped", "Stopped"),
        ("Yawning", "Yawning"),
        ("Drowsiness", "Drowsiness"),
        ("MissingFace", "MissingFace"),
    )

    devices = models.ForeignKey(RaspDevice, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=STATUS)
    timeOccured = models.DateTimeField(null=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    isRead = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.devices.name} - {self.name} at {self.timeOccured}"


class ActiveCheck(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["time"], name="timeActive"),
        ]

    device = models.ForeignKey(RaspDevice, null=True, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.device} was last active on {self.time}"


class Drive(models.Model):
    STATUS = (
        ("ongoing", "ongoing"),
        ("ended", "ended"),
    )
    device = models.ForeignKey(RaspDevice, null=True, on_delete=models.CASCADE)
    startTime = models.DateTimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    endTime = models.DateTimeField(null=True)

    def __str__(self):
        return f"Drive #{self.id} by {self.device}"


class Alert(models.Model):
    DECTECT_TYPE = (
        ("Yawning", "Yawning"),
        ("Drowsiness", "Drowsiness"),
        ("MissingFace", "MissingFace"),
    )
    drive = models.ForeignKey(Drive, null=True, on_delete=models.CASCADE)
    detect = models.CharField(max_length=50, choices=DECTECT_TYPE)
    timeOccured = models.DateTimeField(null=True)

    def __str__(self):
        return f"Drowsiness detection with drive {self.drive.id}"
