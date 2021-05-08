from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from accounts.models import RaspDevice

import json
from datetime import datetime


class RealTime(WebsocketConsumer):
    def updatePiConnection(self, online=True):
        self.pi.status = "online" if online else "offline"
        self.pi.save()

        carLiscense = self.pi.car.licensePlate
        self.sendSignal({
            "messageType": "status",
            "licensePlate": carLiscense,
            "status": online
        })

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["roomCode"]
        self.piID = str(self.scope["url_route"]["kwargs"]["piID"])
        self.pi = False

        if self.piID != "none":
            self.pi = RaspDevice.objects.get(id=self.piID)
            self.updatePiConnection()
            print(self.pi, "is connected")
    

        # print(self.room_name, self.piID, self.scope)
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if self.pi:
            self.updatePiConnection(online=False)
            print(self.pi, "is disconnected")
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        self.sendSignal(data)

    # Send message to all groups
    def sendSignal(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_name, {"type": "randomFunc", "message": message}
        )

    def randomFunc(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))