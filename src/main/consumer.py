from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import json
from datetime import datetime

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
        data = json.loads(event['value'])

        piName = data['name']
        status = data.get('status')
        message = data.get('message')
        time = data.get('time')

        if status is not None:
            piDevice = await self.changePiStatus(piName, status)

        if message is not None:
            await self.saveActivity(piName, message, time)

        await self.send(event['value'])

    @database_sync_to_async
    def changePiStatus(self, piName, status):
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)
        device.status = status
        device.save()
        return result

    @database_sync_to_async
    def saveActivity(self, piName, activity, time):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)

        try:
            Activity.objects.create(devices=device,
                                    activityName=activity,
                                    timeOccured=time)
        except Exception as e:
            print(str(e))
