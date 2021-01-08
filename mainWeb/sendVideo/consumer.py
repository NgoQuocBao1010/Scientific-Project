from channels.generic.websocket import AsyncWebsocketConsumer
import json
import base64


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
        imgEncode = str.encode(imgByte)
        name = data['imgName']
        
        data['noti'] = 'Nhan duoc roi!!!!'
        event['value'] = json.dumps(data)
            

        with open(f"static/images/{name}.png","wb") as f:
            f.write(base64.decodebytes(imgEncode))

        # with open(f"static/images/testPic2.png","wb") as f:
        #     f.write(base64.decodebytes(imgEncode))

        await self.send(event['value'])