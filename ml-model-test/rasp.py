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
        MAXIMUM_NUMBER_OF_SEND_FRAMES = 20
        LIST_OF_FRAMES = []
        cap = cv2.VideoCapture('testVideo.mp4')
        time.sleep(2)

        i = -1
        while True:
            if cv2.waitKey(25) == 13:
                break

            ret, frame = cap.read()
            i += 1
            if i % 1 != 0:
                continue
            
            cv2.putText(frame, f"{i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)
            cv2.imshow('frame', frame)
            _, im_arr = cv2.imencode('.jpg', frame)
            im_bytes = im_arr.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            im_data_str = im_b64.decode('utf-8')

            LIST_OF_FRAMES.append(im_data_str)

            if len(LIST_OF_FRAMES) == MAXIMUM_NUMBER_OF_SEND_FRAMES:
                current_time = str(datetime.datetime.now())
                current_time = current_time.replace(" ", "_").replace(".", "_").replace("-", "_").replace(":", "_")

                print('\n\n\n\n', type(LIST_OF_FRAMES), '\n\n\n\n')
                pp = json.dumps({
                    'imgByte': LIST_OF_FRAMES,
                    'imgName': current_time
                })
                LIST_OF_FRAMES = []
                try:
                    time.sleep(0.3)
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
    url = 'ws://localhost:8000/ws/sendVideo/'
    # url = 'ws://192.168.123.147:8000/ws/sendVideo/'
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()