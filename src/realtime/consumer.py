from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import reverse

from accounts.models import RaspDevice
from .models import *

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    # Update when Raspberry Pi is connected and disconnected
    def updatePiConnection(self, online=True):
        self.pi.status = "online" if online else "offline"
        self.pi.save()

        if online:
            try:
                Drive.objects.create(
                    device=self.pi, startTime=datetime.now(), status="ongoing"
                )
            except Exception as e:
                print(str(e))
        else:
            drive = self.pi.drive_set.all().get(status="ongoing")
            drive.status = "ended"
            drive.endTime = datetime.now()
            drive.save()

        carLiscense = self.pi.car.licensePlate
        self.sendSignal(
            {"messageType": "status", "licensePlate": carLiscense, "status": online}
        )

    # Save neccessary data when alerts is detected
    def alertDetected(self, data):
        alertType = data["name"]
        timeOccured = data["time"]
        drive = self.pi.drive_set.all().get(status="ongoing")
        carLiscense = self.pi.car.licensePlate

        driveUrl = reverse("driveDetail", kwargs={'id': drive.id})

        try:
            Alert.objects.create(drive=drive, detect=alertType, timeOccured=timeOccured)
            print(f"Deteced {alertType} and saved!!")
        except Exception as e:
            print(str(e))

        self.sendSignal(
            {
                "messageType": "notification",
                "alertType": alertType,
                "licensePlate": carLiscense,
                "time": timeOccured,
                "driveUrl": driveUrl,
            }
        )

    commands = {
        "alert": alertDetected,
    }

    # ------------------- Websocket Method -------------------#
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["roomCode"]
        self.piID = str(self.scope["url_route"]["kwargs"]["piID"])
        self.pi = False

        if self.piID != "none":
            self.pi = RaspDevice.objects.get(id=self.piID)
            self.updatePiConnection()
            print(self.pi, "is connected")

        # print(self.room_name, self.piID, self.scope)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.pi:
            self.updatePiConnection(online=False)
            print(self.pi, "is disconnected\n")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    # Send message to all groups
    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "randomFunc", "message": message}
        )

    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))