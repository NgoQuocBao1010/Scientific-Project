import websocket


import _thread as thread

import time
from datetime import datetime
import json
import random

import socket

HOSTNAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOSTNAME)
COMPANY_ROOM_CODE = "lsRHGGT111"
ID = "1"


def on_message(ws, message):
    data = json.loads(message)
    print(data)


def on_error(ws, error):
    # print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(5)
            ws.send(
                json.dumps(
                    {
                        "command": "alert",
                        "name": random.choice(["Yawning", "Drowsiness"]),
                        "time": str(datetime.now()),
                    }
                )
            )
            break
        ws.close()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = f"ws://{HOSTNAME}:8000/ws/realtime/{COMPANY_ROOM_CODE}/{NAME}/"
    url = f"ws://localhost:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"

    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()