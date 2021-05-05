from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from accounts.models import RaspDevice
from .models import Drive, Alert

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    # Update the last time the system receive signal from pi
    def updateActive(self, data):
        piName = data.get("name")
        activeTime = datetime.now()
        result = RaspDevice.objects.all()
        device = result.get(name=piName)
        print(self.scope["client"])

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

    # check if pi was disconnected
    def checkActive(self, data):
        piDevices = RaspDevice.objects.filter(status="online")
        disDevices = []
        disconnect = False

        for pi in piDevices:
            disconnect = False
            lastActive = pi.lastActive
            print(f"{datetime.now()}\t{lastActive}\t{pi.name}")
            if datetime.now().minute - lastActive.minute < 1:
                if datetime.now().second - lastActive.second >= 20:
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
        piName = data.get("name")
        detect = data.get("activity")
        time = data.get("time")

        pi = RaspDevice.objects.get(name=piName)
        drive = pi.drive_set.all().get(status="ongoing")

        try:
            Alert.objects.create(drive=drive, detect=detect, timeOccured=time)
            print("Deteced and saved!!")
        except Exception as e:
            print(str(e))

        self.sendSignal(data)

    def getInfo(self, data):
        self.sendSignal(data)

    def sendVideo(self, data):
        self.sendSignal(data)

    # Test
    def testActive(self, data):
        pass

    def testActive2(self, client):
        ipAddress, port = client
        try:
            device = RaspDevice.objects.get(ipAddress=ipAddress)

            device.status = "online"
            device.lastActive = datetime.now()
            device.save()
            print(f"{device} is online")
        except Exception as e:
            print("Not a Pi")

    def testDis(self, client):
        ipAddress, port = client
        try:
            device = RaspDevice.objects.get(ipAddress=ipAddress)

            device.status = "offline"
            device.lastActive = datetime.now()
            device.save()
            print(f"{device} is offline")
        except Exception as e:
            print("Not a Pi")

    commands = {
        "check": checkActive,
        "updateActive": updateActive,
        "alert": drowsinessDetect,
        "getInfo": getInfo,
        "send_video": sendVideo,
        # test
        "testActive": testActive,
    }

    def connect(self):
        self.group_name = "realtime"
        self.testActive2(self.scope["client"])

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        self.testDis(self.scope["client"])

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
