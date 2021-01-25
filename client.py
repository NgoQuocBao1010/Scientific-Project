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
DEVICES_NAME = 'Pi 1'


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
        global ONLINE, DEVICES_NAME
        if not ONLINE:
            message = json.dumps({
                'status': 'Online',
                'name': DEVICES_NAME,
                'time': str(datetime.now()),
                'message': 'Starting',
            })

            try:
                ws.send(message)
            except Exception as e:
                print(str(e))

            ONLINE = True

        lastActive = datetime.now()

        dumpMsg = 1
        while ONLINE:
            time.sleep(1)
            if dumpMsg > 10:
                ONLINE = False
                break

            if datetime.now().second - lastActive.second >= SENCOND_SEND:
                message = json.dumps({
                    'name': DEVICES_NAME,
                    'active': str(datetime.now())
                })

                lastActive = datetime.now()

                try:
                    ws.send(message)
                except Exception as e:
                    print(str(e))

            dumpMsg += 1

        ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    url = 'ws://localhost:8000/ws/realtimeData/'

    ws = websocket.WebSocketApp(url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()