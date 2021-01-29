from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
import time
import json
from datetime import datetime

from .models import *


class RealtimeData(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'realtimeData'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):  # changed
        # time.sleep(6)
        # pi = await self.checkActive()
        await self.channel_layer.group_discard(group='realtimeData',
                                               channel=self.channel_name)
        await super().disconnect(code)

        # await self.receive(json.dumps({'name': pi, 'status': 'Offline'}))

    async def receive(self, text_data):
        await self.channel_layer.group_send(self.group_name, {
            'type': 'randomFuntion',
            'value': text_data,
        })

    async def randomFuntion(self, event):
        data = json.loads(event['value'])

        piName = data.get('name')
        activeTime = data.get('activeTime')

        if activeTime is not None:
            await self.updateActive(piName, activeTime)

        activity = data.get('activity')
        time = data.get('time')
        if activity is not None:
            await self.saveActivity(piName, activity, time)

        check = data.get('check')
        if check is not None:
            await self.checkActive()
        await self.send(event['value'])

    @database_sync_to_async
    def checkActive(self):
        print('Check for disconnect devices')
        piDevices = RaspberryDevice.objects.all().filter(status='Online')

        for pi in piDevices:
            lastActive = pi.lastActive
            # print(f'{datetime.now()}\n{lastActive}')
            if datetime.now().minute - lastActive.minute < 1:
                if datetime.now().second - lastActive.second >= 6:
                    print(pi.name, 'is disconnect')
                    pi.status = 'Offline'
                    pi.save()

            else:
                print(pi.name, 'is disconnect')
                pi.status = 'Offline'
                pi.save()

    @database_sync_to_async
    def updateActive(self, piName, activeTime):
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)

        if device.lastActive != activeTime:
            print('Update', device.name)
            device.lastActive = activeTime

            if device.status == 'Offline':
                device.status = 'Online'

            device.save()

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
