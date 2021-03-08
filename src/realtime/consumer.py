from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from accounts.models import RaspDevice

import json


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
