import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
from datetime import datetime
import json
import random

SENCOND_SEND = 5
ONLINE = False
DEVICES_NAME = 'AI Server'


def on_message(ws, message):
    data = json.loads(message)
    # print(data['noti'])


def on_error(ws, error):
    # print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        pass


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = 'ws://localhost:8000/ws/realtimeData/'
    url = 'ws://192.168.123.149:8000/ws/realtimeData/'

    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()