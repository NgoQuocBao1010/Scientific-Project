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
