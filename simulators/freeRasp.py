import websocket
import os
from PIL import Image
import _thread as thread
from io import BytesIO
import time
from datetime import datetime
import json
import random
import base64
import socket

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
ID = "10"


def on_message(ws, message):
    data = json.loads(message)

    if data["id"] == ID:
        print('Done!!!')
        
    ws.close()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):

    print(f"### closed on {close_msg} ###")


def on_open(ws):
    def run(*args):
        ws.send(
            json.dumps(
                {
                    "command": "getRoomCode",
                    "id": str(ID),
                }
            )
        )

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    url = f"ws://{HOSTNAME}:8000/ws/realtime/general/{ID}/"
    # url = f"ws://localhost:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"

    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()