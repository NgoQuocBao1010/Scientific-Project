import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import cv2
import datetime
import base64
from picamera.array import PiRGBArray
from picamera import PiCamera

def on_message(ws, message):
    data = json.loads(message)
    # print(data['noti'])


def on_error(ws, error):
    print(error)
    pass


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        # cap = cv2.VideoCapture(0)
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))

        i = -1
        time.sleep(1.5)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = frame.array
            if cv2.waitKey(25) == 13:                                                                                                   break
            rawCapture.truncate()
            rawCapture.seek(0)

            i += 1
            if i % 1 != 0:
                continue

            # cv2.imshow('frame', frame)
            _, im_arr = cv2.imencode('.jpg', frame)
            im_bytes = im_arr.tobytes()
             im_b64 = base64.b64encode(im_bytes)
            im_data_str = im_b64.decode('utf-8')

            current_time = str(datetime.datetime.now())
            current_time = current_time.replace(" ", "_").replace(".", "_").replace("-", "_").replace(":", "_")

            pp = json.dumps({
                'imgByte': im_data_str,
                'imgName': current_time
            })
            print(pp)
            try:
                ws.send(pp)
            except Exception as e:
                print(str(e))                                                                                                   # cap.release()
        # cv2.destroyAllWindows()
        ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    # url = 'ws://localhost:8000/ws/sendVideo/'
    url = 'ws://192.168.123.147:8000/ws/sendVideo/'
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

