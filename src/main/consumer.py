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
        print(data)

        piName = data.get('name')
        time = data.get('time')
        if time is not None:
            await self.updateActive(piName, time)

        activity = data.get('activity')
        if activity is not None:
            await self.saveActivity(piName, activity, time)

        check = data.get('check')
        if check is not None:
            disDevices = await self.checkActive()

            if len(disDevices) > 0:
                await self.receive(json.dumps({'dis': disDevices}))

        await self.send(event['value'])

    @database_sync_to_async
    def checkActive(self):
        piDevices = RaspberryDevice.objects.all().filter(status='Online')
        disDevices = []
        disconnect = False

        for pi in piDevices:
            lastActive = pi.lastActive
            print(f'{datetime.now()}\n{lastActive}')
            if datetime.now().minute - lastActive.minute < 1:
                if datetime.now().second - lastActive.second >= 10:
                    disconnect = True

            else:
                disconnect = True

            if disconnect:
                print(pi.name, 'is disconnect')
                disDevices.append(pi.name)
                pi.status = 'Offline'
                pi.save()
                try:
                    Activity.objects.create(devices=pi,
                                            activityName='Stopped',
                                            timeOccured=datetime.now())
                except Exception as e:
                    print(str(e))

        return disDevices

    @database_sync_to_async
    def updateActive(self, piName, activeTime):
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)

        if device.lastActive != activeTime:
            print('Update', device.name, activeTime)
            device.lastActive = activeTime

            if device.status == 'Offline':
                device.status = 'Online'
                try:
                    Activity.objects.create(devices=device,
                                            activityName='Starting',
                                            timeOccured=activeTime)
                except Exception as e:
                    print(str(e))

            device.save()

    @database_sync_to_async
    def saveActivity(self, piName, activity, time):
        print('Saving', activity, 'in', piName)
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        result = RaspberryDevice.objects.all()
        device = result.get(name=piName)

        try:
            Activity.objects.create(devices=device,
                                    activityName=activity,
                                    timeOccured=time)
        except Exception as e:
            print(str(e))
