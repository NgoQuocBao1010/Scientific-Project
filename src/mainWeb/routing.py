from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from sendVideo import consumer

ws_patterns = [
    path('ws/sendVideo/', consumer.SendVideo.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        'websocket': AuthMiddlewareStack(URLRouter(ws_patterns))
    }
)