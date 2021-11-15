from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.urls import reverse

from accounts.models import RaspDevice
from accounts.customPrint import MyCustomPrint
from .models import *

import json
from datetime import datetime

class RealTime(WebsocketConsumer):
    def updatePiConnection(self, online=True):
        """ Update when Raspberry Pi is connected and disconnected """
        driveID =  None

        # Check if user add car to rasp during the drive
        if not online:
            checkRasp = RaspDevice.objects.get(id=self.pi.id)
            self.pi = checkRasp

        self.pi.status = "online" if online else "offline"
        self.pi.save()

        if not online and not self.pi.car:
            return
        
        if online:  # Update new drive to database 
            try:
                newDrive = Drive.objects.create(
                    device=self.pi, startTime=datetime.now(), status="ongoing"
                )
                driveID = newDrive.id
                driveUrl = reverse("driveDetail", kwargs={'id': driveID})
                MyCustomPrint(f"New Drive {driveID} is added")

            except Exception as e:
                MyCustomPrint(str(e), style="error")
        
        else:  # End the ongoing drives when there is car
            drive = self.pi.drive_set.all().order_by('-startTime')[0]
            drive.status = "ended"
            drive.endTime = datetime.now()
            driveID = drive.id
            driveUrl = reverse("driveDetail", kwargs={'id': driveID})
            drive.save()

            MyCustomPrint(f"Drive {driveID} is ended")

        if not self.pi.car:
            MyCustomPrint(f"Activity from {self.pi} that has no car!", style="warning")
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


    def alertDetected(self, data):
        """ Save neccessary data when alerts is detected """
        if self.unsignedPi:
            return
        
        alertType = data["name"]
        timeOccured = data["time"]
        drives = self.pi.drive_set.all().order_by('-startTime')

        if not drives:
            return
        
        drive = drives[0]

        checkRasp = RaspDevice.objects.get(id=self.pi.id)
        if not self.pi.car and checkRasp.car:
            self.pi = checkRasp

        if not self.pi.car:
            MyCustomPrint(f"Drowsiness detection from {self.pi} that has no car!", style="warning")
            carLiscense = "Xe không xác định"
        else:
            carLiscense = self.pi.car.licensePlate

        driveUrl = reverse("driveDetail", kwargs={'id': drive.id})

        try:
            Alert.objects.create(drive=drive, detect=alertType, timeOccured=timeOccured)
            MyCustomPrint(f"Deteced {alertType} from {drive} and saved!!", style="warning")
        except Exception as e:
            MyCustomPrint(str(e), style="error")

        self.sendSignal(
            {
                "messageType": "notification",
                "alertType": alertType,
                "licensePlate": carLiscense,
                "time": timeOccured,
                "driveUrl": driveUrl,
            }
        )


    def getVideo(self, data):
        """ Get video message """
        driveID = data["driveID"]
        drive = Drive.objects.get(id=driveID)
        alerts = drive.alert_set.all().exclude(detect="Alcohol").order_by('-timeOccured')

        if len(alerts) > 0:
            data.setdefault("time-occured", str(alerts[0].timeOccured))
            data.setdefault("alertType", str(alerts[0].detect))
            self.sendSignal(data)
            MyCustomPrint(f"Request video from {drive.device}")
    

    def sendImgToBrowser(self, data):
        """ Send image data to the browser to display """
        self.sendSignal(data)
        MyCustomPrint(f"Sending videos")
    
    def getRoomCode(self, data):
        """ send room code to unconfig rasp """
        if self.unsignedPi:
            if self.pi.company:
                roomCode = self.pi.company.roomCode
                data.setdefault("roomCode", roomCode)

                self.sendSignal(data)
                MyCustomPrint("Room code is sent to the rasp!!", style="success")
            else:
                MyCustomPrint(f"Can't send room code to {self.pi}, no room field in database", style="warning")

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
            MyCustomPrint(f"Pi is in general room")
            self.unsignedPi = True
        
        if self.piID != "none":
            self.pi = RaspDevice.objects.get(id=self.piID)
            MyCustomPrint(f"{self.pi} is connected")
            if not self.unsignedPi: self.updatePiConnection()

        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.pi and not self.unsignedPi:
            if not self.unsignedPi: self.updatePiConnection(online=False)
            MyCustomPrint(f"{self.pi} is disconnected!")

        async_to_sync(self.channel_layer.group_discard)(
            self.room_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "randomFunc", "message": message}
        )

    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))