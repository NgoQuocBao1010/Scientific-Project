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
ID = "1"

# baseDir = os.path.abspath(os.path.dirname(__file__))
# path = os.path.join(baseDir, "roomcode.cfg")

ROOM_CODE = "general"
# with open(path, "r") as file:
#     ROOM_CODE = file.read()


MESSAGE = {
    "roomCode": {
        "command": "getRoomCode",
        "piDeviceID": str(ID),
    },
    "alert": {
        "command": "alert",
        "name": "Drowsiness",
        "time": str(datetime.now()),
    }
}

def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def connectToWebsocket(url):
    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()


def on_open(ws):
    def run(*args):
        # Sending request to get room code
        if ROOM_CODE == "general":
            ws.send(
                json.dumps(MESSAGE.get("roomCode"))
            )
            print(f"Sending request to get room code")
        # Detecting drowsiness if room code is received
        else:
            print("Detecting Drowsiness ....")
            time.sleep(3)
            ws.send(
                json.dumps(
                    MESSAGE.get("alert")
                )
            )

    thread.start_new_thread(run, ())

def convertImgToByte():
    imgFolder = "./simulators/images/"
    images = os.listdir(imgFolder)

    imgBytes = []
    for image in images:
        imageUrl = os.path.join(imgFolder, image)
        image = Image.open(imageUrl) 
        resized_image = image.resize((640, 464))
        im_file = BytesIO()
        resized_image.save(im_file, format="PNG")
        im_bytes = im_file.getvalue()
        imgBytes.append(im_bytes)
    
    return imgBytes

def on_message(ws, message):
    global ROOM_CODE
    data = json.loads(message)
    # print(f"Message: {data}")

    if int(data["piDeviceID"]) == int(ID):
        if data["command"] == "getRoomCode":
            ROOM_CODE = data["roomCode"]
            ws.close()
            newUrl = f"ws://localhost:8000/ws/realtime/{ROOM_CODE}/{ID}/"
            print("Room code Received")
            connectToWebsocket(newUrl)
        
        if data["command"] == "getVideo":
            images = convertImgToByte()

            for imgByte in images:
                try:
                    f_data = base64.b64encode(imgByte).decode("utf-8")
                    ws.send(
                        json.dumps(
                            {
                                "command": "sendImgToBrowser",
                                "messageType": "sendImg",
                                "driveID": data["driveID"],
                                "frame": str(f_data),
                                "time-happened": str(datetime.now()),
                            }
                        )
                    )
                except Exception as e:
                    print(str(e))
            print("Sent all images")


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = f"ws://{HOSTNAME}:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"
    url = f"ws://localhost:8000/ws/realtime/{ROOM_CODE}/{ID}/"
    connectToWebsocket(url)