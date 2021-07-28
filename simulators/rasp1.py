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
COMPANY_ROOM_CODE = "lsRHGGT111"
ID = "1"


def on_message(ws, message):
    thisFolder = "./simulators/images/"
    data = json.loads(message)

    if data.get("piDeviceID") == ID:
        images = os.listdir(thisFolder)

        for image in images:
            imageUrl = os.path.join(thisFolder, image)
            image = Image.open(imageUrl) 
            resized_image = image.resize((640, 464))
            im_file = BytesIO()
            resized_image.save(im_file, format="PNG")
            im_bytes = im_file.getvalue()

            try:
                f_data = base64.b64encode(im_bytes).decode("utf-8")
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
                print("Sent image", imageUrl)
            except Exception as e:
                print(str(e))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):

    print(f"### closed on {close_msg} ###")


def on_open(ws):
    def run(*args):
        time.sleep(2)
        ws.send(
            json.dumps(
                {
                    "command": "alert",
                    "name": random.choice(["Alcohol", "Drowsiness", "Noeye"]),
                    "time": str(datetime.now()),
                }
            )
        )
        time.sleep(1)
        
        ws.close()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = f"ws://{HOSTNAME}:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"
    url = f"ws://localhost:8000/ws/realtime/{COMPANY_ROOM_CODE}/{ID}/"

    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()
