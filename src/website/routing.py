from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from realtime import consumer

ws_patterns = [
    re_path(
        r"ws/realtime/(?P<roomCode>\w+)/(?P<piID>\w+)/$", consumer.RealTime.as_asgi()
    ),
]

application = ProtocolTypeRouter(
    {"websocket": AuthMiddlewareStack(URLRouter(ws_patterns))}
)