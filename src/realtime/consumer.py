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

        if not self.pi.car and not online:
            checkRasp = RaspDevice.objects.get(id=self.pi.id)
            if checkRasp.car:
                self.pi = checkRasp

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

        if not self.pi.car:
            print(f"\n[SERVER]: Activity from {self.pi} that has no car!\n")
            carLiscense = "Xe không xác định"
        else:
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

        if not self.pi.car:
            print(f"\n[SERVER]: Drowsiness detection from {self.pi} that has no car!\n")
            carLiscense = "Xe không xác định"
        else:
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
    
    # Display image to browser
    def sendImgToBrowser(self, data):
        self.sendSignal(
            data
        )
    
    # send room code to unconfig rasp
    def getRoomCode(self, data):
        if self.unsignedPi:
            if self.pi.company:
                roomCode = self.pi.company.roomCode
                data.setdefault("roomCode", roomCode)

                self.sendSignal(
                    data
                )
                print("\n[SERVER] Room code is sent to the rasp!!\n")
            else:
                print(f"\n[SERVER] Can't send room code to {self.pi} cuz there no room field!!\n")

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
            print(f"\n[SERVER]: Pi is in general room\n")
            self.unsignedPi = True
        
        if self.piID != "none":
            self.pi = RaspDevice.objects.get(id=self.piID)
            if not self.unsignedPi: self.updatePiConnection()
            print(f"\n[SERVER]: {self.pi} is connected\n")

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.pi and not self.unsignedPi:
            if not self.unsignedPi: self.updatePiConnection(online=False)
            print(f"\n[SERVER]: {self.pi} is disconnected!\n")

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