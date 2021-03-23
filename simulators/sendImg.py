import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time
from datetime import datetime
import json, base64
import random

SENCOND_SEND = 5
DEVICES_NAME = "Pi 1"


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
        with open("nchm.png", "rb") as f:
            f_data = base64.b64encode(f.read()).decode("utf-8")

        try:
            ws.send(
                json.dumps(
                    {
                        "command": "send_video",
                        "name": DEVICES_NAME,
                        "frame": str(f_data),
                    }
                )
            )
            print("Da send")
        except Exception as e:
            print(str(e))

        # print("thread terminating...")

        ws.close()

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = "ws://localhost:8000/ws/realtime/"
    # url = "ws://10.10.32.119:8000/ws/realtime/"
    url = "ws://192.168.123.147:8000/ws/realtime/"

    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()