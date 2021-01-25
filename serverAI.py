import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
from datetime import datetime
import json
import random
import cv2

ONLINE = False
DEVICES_NAME = 'Pi 1'


def on_message(ws, message):
    data = json.loads(message)


def on_error(ws, error):
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

        webcam = cv2.VideoCapture(0)
        time.sleep(1.5)

        trackingFrame = 0
        statusDetect = 1

        # Send realtime message
        while ONLINE:
            ret, frame = webcam.read()

            if not ret:
                ONLINE = False
                break

            trackingFrame += 1
            status = ['Yawning', 'Drowsiness']
            cv2.imshow('Frame', frame)
            deviceStatus = random.choice(status)
            timeOccured = datetime.now()

            if trackingFrame % 1113 == 0:
                deviceStatus = random.choice(status)

                message = json.dumps({
                    'message': str(deviceStatus),
                    'name': DEVICES_NAME,
                    'time': str(timeOccured)
                })

                try:
                    ws.send(message)
                except Exception as e:
                    print(str(e))

            if trackingFrame % 20 == 0:
                message = json.dumps({
                    'name': DEVICES_NAME,
                    'active': 1,
                    'time': str(timeOccured)
                })

                try:
                    ws.send(message)
                except Exception as e:
                    print(str(e))

            if cv2.waitKey(1) == 27:
                break  # esc to quit

        cv2.destroyAllWindows()

        # Detect Disconnect
        # Dump way
        time.sleep(1)
        message = json.dumps({
            'status': 'Offline',
            'name': DEVICES_NAME,
            'time': str(datetime.now()),
            'message': 'Stopped',
        })
        try:
            print('Offline message!!!!')
            ws.send(message)
        except Exception as e:
            print(str(e))

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