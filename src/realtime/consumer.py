from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.piName = self.scope["url_route"]["kwargs"]["pi"]

        print(self.room_name, self.piName)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.sendSignal(data)

    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "randomFunc", "message": message}
        )

    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))