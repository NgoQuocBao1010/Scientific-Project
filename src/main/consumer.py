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

    # async def disconnect(self, event):
    #     print('disconnected! ', event)

    async def disconnect(self, code):  # changed
        await self.checkActive()
        await self.channel_layer.group_discard(group='realtimeData',
                                               channel=self.channel_name)
        await super().disconnect(code)

    async def receive(self, text_data):
        # print(text_data)

        await self.channel_layer.group_send(self.group_name, {
            'type': 'randomFuntion',
            'value': text_data
        })

    async def randomFuntion(self, event):
        data = json.loads(event['value'])
        print(data)

        piName = data['name']
        status = data.get('status')
        message = data.get('message')
        time = data.get('time')
        active = data.get('active')

        if active is not None:
            await self.updateActive(piName, active)

        if status is not None:
            piDevice = await self.changePiStatus(piName, status)

        if message is not None:
            await self.saveActivity(piName, message, time)

        await self.send(event['value'])

    @database_sync_to_async
    def checkActive(self):
        print('Check for disconnect devices')
        checkTime = 6
        time.sleep(checkTime)
        piDevices = RaspberryDevice.objects.all()

        for pi in piDevices:
            if pi.status == 'Offline':
                continue

            lastActive = pi.lastActive
            if datetime.now().minute - lastActive.minute < 1:
                if datetime.now().second - lastActive.second > checkTime:
                    print(pi.name, 'is disconnect')
                    pi.status = 'Offline'
                    pi.save()
                    message = json.dumps({'haha': 'haha'})
                    self.send(message)

            else:
                print(pi.name, 'is disconnect')
                pi.status = 'Offline'
                pi.save()
                message = json.dumps({'haha': 'haha'})
                self.send(message)

        print('Done')

    @database_sync_to_async
    def changePiStatus(self, piName, status):
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)
        device.status = status
        device.save()

    @database_sync_to_async
    def updateActive(self, piName, lastActive):
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)

        if device.lastActive != lastActive:
            device.lastActive = lastActive
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
