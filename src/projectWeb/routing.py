from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from realtime import consumer2

ws_patterns = [
    path("ws/realtime/", consumer2.RealTime.as_asgi()),
]

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(ws_patterns))}
)