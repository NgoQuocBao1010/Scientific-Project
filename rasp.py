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
        cap = cv2.VideoCapture(0)

        i = -1
        while True:
            if cv2.waitKey(25) == 13:
                break

            ret, frame = cap.read()
            i += 1
            if i % 30 != 0:
                continue
            
            cv2.imshow('frame', frame)
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
            try:
                ws.send(pp)
            except Exception as e:
                print(str(e))
        cap.release()
        cv2.destroyAllWindows()
        ws.close()
        # print("thread terminating...")

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    url = 'ws://192.168.1.21:8000/ws/sendVideo/'
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()