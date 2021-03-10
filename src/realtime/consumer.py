from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from accounts.models import RaspDevice
from .models import Activity

import json
from datetime import datetime


class RealTime(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "realtime"

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # print(text_data)

        await self.channel_layer.group_send(
            self.group_name, {"type": "randomFuntion", "value": text_data}
        )

    async def randomFuntion(self, event):
        print(event["value"])
        data = json.loads(event["value"])

        piName = data.get("name")
        time = data.get("time")
        if time is not None:
            await self.updateActive(piName, time)

        check = data.get("check")
        if check is not None:
            disDevices = await self.checkActive()

            if len(disDevices) > 0:
                await self.receive(json.dumps({"dis": disDevices}))

        await self.send(event["value"])

    @database_sync_to_async
    def updateActive(self, piName, activeTime):
        result = RaspDevice.objects.all()
        device = result.get(name=piName)

        if device.lastActive != activeTime:
            print("Update", device.name, activeTime)
            device.lastActive = activeTime

            if device.status == "offline":
                device.status = "online"
                device.save()

                try:
                    Activity.objects.create(
                        devices=device, name="Starting", timeOccured=activeTime
                    )
                except Exception as e:
                    print(str(e))

    @database_sync_to_async
    def checkActive(self):
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
                disDevices.append(pi.name)
                pi.status = "offline"
                pi.save()

                try:
                    Activity.objects.create(
                        devices=pi, name="Stopped", timeOccured=datetime.now()
                    )
                except Exception as e:
                    print(str(e))

        return disDevices
