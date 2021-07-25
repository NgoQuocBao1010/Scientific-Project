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
ID = "17"

baseDir = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(baseDir, "roomcode.cfg")

ROOM_CODE = None
with open(path, "r") as file:
    ROOM_CODE = file.read()


MESSAGE = {
    "roomCode": {
        "command": "getRoomCode",
        "id": str(ID),
    },
    "alert": {
        "command": "alert",
        "name": random.choice(["Alcohol", "Drowsiness"]),
        "time": str(datetime.now()),
    }
}



def on_message(ws, message):
    global ROOM_CODE
    data = json.loads(message)
    print(data)

    if int(data["id"]) == int(ID):
        print("Change room code ...")
        with open(path, "w") as file:
            file.write(data["roomCode"])
        
        ROOM_CODE = data["roomCode"]
        ws.close()
        newUrl = f"ws://localhost:8000/ws/realtime/{ROOM_CODE}/{ID}/"
        connectToWebsocket(newUrl)



def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        if ROOM_CODE == "general":
            ws.send(
                json.dumps(
                    MESSAGE.get("roomCode")
                )
            )
            print(f"In room {ROOM_CODE}")
        else:
            print("Detecting Drowsiness ....")
            time.sleep(3)
            ws.send(
                json.dumps(
                    MESSAGE.get("alert")
                )
            )

    thread.start_new_thread(run, ())


def connectToWebsocket(url):
    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = f"ws://{HOSTNAME}:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"
    url = f"ws://localhost:8000/ws/realtime/{ROOM_CODE}/{ID}/"
    connectToWebsocket(url)