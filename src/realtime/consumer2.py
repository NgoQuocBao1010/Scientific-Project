from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from accounts.models import RaspDevice
from .models import Drive, Alert

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    def updateActive(self, data):
        piName = data.get("name")
        activeTime = data.get("time")
        result = RaspDevice.objects.all()
        device = result.get(name=piName)

        if device.lastActive != activeTime:
            print("Update", device.name, activeTime)
            device.lastActive = activeTime

            if device.status == "offline":
                device.status = "online"

                try:
                    Drive.objects.create(
                        device=device, startTime=activeTime, status="ongoing"
                    )
                except Exception as e:
                    print(str(e))

                self.sendSignal(data)

            device.save()

    def checkActive(self, data):
        piDevices = RaspDevice.objects.filter(status="online")
        disDevices = []
        disconnect = False

        for pi in piDevices:
            disconnect = False
            lastActive = pi.lastActive
            print(f"{datetime.now()}\t{lastActive}\t{pi.name}")
            if datetime.now().minute - lastActive.minute < 1:
                if datetime.now().second - lastActive.second >= 10:
                    disconnect = True

            else:
                disconnect = True

            if disconnect:
                print(pi.name, "is disconnect")
                drive = pi.drive_set.all().get(status="ongoing")

                disDevices.append(pi.name)
                pi.status = "offline"
                pi.save()

                try:
                    drive.status = "ended"
                    drive.endTime = datetime.now()
                    drive.save()
                except Exception as e:
                    print(str(e))

        if len(disDevices) > 0:
            self.sendSignal({"dis": disDevices, "disTime": str(datetime.now())})

    def drowsinessDetect(self, data):
        alertType = data.get("type")
        device = RaspDevice.objects.get(name=data.get("name"))
        alertTime = RaspDevice.objects.get(name=data.get("alertTime"))
        drive = device.drive_set.all().get(status="ongoing")

        try:
            Alert.objects.create(drive=drive, detect=alertType, alertTime=alertTime)
        except Exception as e:
            print(str(e))

    commands = {
        "check": checkActive,
        "updateActive": updateActive,
        "alert": drowsinessDetect,
    }

    def connect(self):
        self.group_name = "realtime"

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        # print(data)

        self.commands[data["command"]](self, data)

    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "randomFunc", "message": message}
        )

    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))
