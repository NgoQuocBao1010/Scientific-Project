from channels.layers import get_channel_layer
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
        driveID =  None
        self.pi.status = "online" if online else "offline"
        self.pi.save()

        if online:
            try:
                newDrive = Drive.objects.create(
                    device=self.pi, startTime=datetime.now(), status="ongoing"
                )
                driveID = newDrive.id
                driveUrl = reverse("driveDetail", kwargs={'id': driveID})
                print(f"\n[DATABASE]: New Drive {driveID} is added\n")
            except Exception as e:
                print(str(e))
        else:
            drive = self.pi.drive_set.all().order_by('-startTime')[0]
            drive.status = "ended"
            print(f"\n[DATABASE]: Drive {drive.id} is ended\n")
            drive.endTime = datetime.now()
            driveID = drive.id
            driveUrl = reverse("driveDetail", kwargs={'id': driveID})
            drive.save()

        carLiscense = self.pi.car.licensePlate
        self.sendSignal(
            {
                "messageType": "status", 
                "licensePlate": carLiscense, 
                "status": online, 
                "piID": self.pi.id,
                "driveID": driveID,
                "driveUrl": driveUrl,
            }
        )

    # Save neccessary data when alerts is detected
    def alertDetected(self, data):
        if self.unsignedPi:
            return
        
        alertType = data["name"]
        timeOccured = data["time"]
        drive = self.pi.drive_set.all().order_by('-startTime')[0]

        carLiscense = self.pi.car.licensePlate
        driveUrl = reverse("driveDetail", kwargs={'id': drive.id})

        try:
            Alert.objects.create(drive=drive, detect=alertType, timeOccured=timeOccured)
            print(f"\n[DATABASE]: Deteced {alertType} and saved!!\n")
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

    # Get video message
    def getVideo(self, data):
        driveID = data["driveID"]
        drive = Drive.objects.get(id=driveID)
        alerts = drive.alert_set.all().order_by('-timeOccured')

        if len(alerts) > 0:
            # print(alerts[0].timeOccured)
            data.setdefault("time-occured", str(alerts[0].timeOccured))

            self.sendSignal(
                data
            )
    
    def sendImgToBrowser(self, data):
        self.sendSignal(
            data
        )
    
    # send room code to unconfig rasp
    def getRoomCode(self, data):
        if self.unsignedPi:
            print("[ROOMCODE] Room code is sent to the rasp!!")
            roomCode = self.pi.company.roomCode
            data.setdefault("roomCode", roomCode)

            self.sendSignal(
                data
            )
        else:
            self.sendSignal(
                {
                    "message": "4123 BAD REQUEST"
                }
            )

    # List of commands
    commands = {
        "alert": alertDetected,
        "getVideo": getVideo,
        "sendImgToBrowser": sendImgToBrowser,
        "getRoomCode": getRoomCode,
    }

    # ------------------- Websocket Method -------------------#
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["roomCode"]
        self.piID = str(self.scope["url_route"]["kwargs"]["piID"])

        self.pi = False
        self.unsignedPi = False
        
        if self.room_name == "general":
            print(f"[SERVER]: Pi is in general room")
            self.unsignedPi = True
        
        if self.piID != "none":
            self.pi = RaspDevice.objects.get(id=self.piID)
            if not self.unsignedPi: self.updatePiConnection()
            print(f"[SERVER]: {self.pi} is connected")

        # print(self.room_name, self.piID, self.scope)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.pi and not self.unsignedPi:
            if not self.unsignedPi: self.updatePiConnection(online=False)
            print(f"[SERVER]: {self.pi} is disconnected!")

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