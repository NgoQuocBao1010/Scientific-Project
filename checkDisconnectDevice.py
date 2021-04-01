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
        lastActive = datetime.now()
        send = False

        try:
            ws.send(json.dumps({"command": "check", "time": str(lastActive)}))
        except Exception as e:
            print(str(e))

        while True:
            if datetime.now().minute - lastActive.minute >= 1:
                send = True

            else:
                if datetime.now().second - lastActive.second >= 10:
                    send = True

            if send:
                print("Dang gui", datetime.now())
                try:
                    ws.send(
                        json.dumps({"command": "check", "time": str(datetime.now())})
                    )
                    send = False
                    lastActive = datetime.now()
                except Exception as e:
                    print(str(e))

        ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    # url = "ws://localhost:8000/ws/realtime/"
    # url = "ws://10.10.36.35:8000/ws/realtime/"
    url = "ws://192.168.123.147:8000/ws/realtime/"

    ws = websocket.WebSocketApp(
        url, on_message=on_message, on_error=on_error, on_close=on_close
    )
    ws.on_open = on_open
    ws.run_forever()