from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64

from .mlModels import usingDeepLearning2
from .drosinessDetect import detectionDrowsiness


class SendVideo(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'sendVideo'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # print(text_data)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'randomFuntion',
                'value': text_data
            }
        )

    async def randomFuntion(self, event):
        # print(event['value'])
        data = json.loads(event['value'])

        imgByte = data['imgByte']
        time = data['imgName']
        data['noti'] = 'Nhan duoc roi!!!!'

        data['imgByte'] = detectionDrowsiness(imgByte, time)
        event['value'] = json.dumps(data)
        await self.send(event['value'])