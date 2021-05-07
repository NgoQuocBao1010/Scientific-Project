from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from realtime import consumer

ws_patterns = [
    path("ws/realtime/", consumer.RealTime.as_asgi()),
]

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(ws_patterns))}
)