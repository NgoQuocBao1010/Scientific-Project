from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    def connect(self):
        self.group_name = "realtime"
        ipAddress, port = self.scope["client"]
        print(ipAddress)
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
    
    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "randomFunc", "message": message}
        )
    
    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))