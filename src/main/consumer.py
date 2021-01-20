from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json

from .models import *


class RealtimeData(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'realtimeData'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # print(text_data)

        await self.channel_layer.group_send(self.group_name, {
            'type': 'randomFuntion',
            'value': text_data
        })

    async def randomFuntion(self, event):
        # print(event['value'])
        data = json.loads(event['value'])

        piName = data['name']

        piDevice = await self.getPiDevice(piName)
        # piDevice = await database_sync_to_async(RaspberryDevice.objects.all)()
        # print(piDevice)

        await self.send(event['value'])

    @database_sync_to_async
    def getPiDevice(self, piName):
        result = RaspberryDevice.objects.all()
        print(result)
        return result
