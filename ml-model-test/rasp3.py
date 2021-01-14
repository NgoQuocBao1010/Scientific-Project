import cv2
import datetime
import base64
import time

from fixModels import detectionDrowsiness


MAXIMUM_NUMBER_OF_SEND_FRAMES = 20
LIST_OF_FRAMES = []



cap = cv2.VideoCapture('testVideo.mp4')
time.sleep(1)

i = -1
while(True):
	i += 1
	# Capture frame-by-frame
	ret, frame = cap.read()

	if not ret:
		detectionDrowsiness(LIST_OF_FRAMES)
		break

	# print(len(LIST_OF_FRAMES))

	_, im_arr = cv2.imencode('.jpg', frame)
	im_bytes = im_arr.tobytes()
	im_b64 = base64.b64encode(im_bytes)
	im_data_str = im_b64.decode('utf-8')

	LIST_OF_FRAMES.append(im_data_str)

	if len(LIST_OF_FRAMES) == MAXIMUM_NUMBER_OF_SEND_FRAMES:
		detectionDrowsiness(LIST_OF_FRAMES)
		LIST_OF_FRAMES = []

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

print(i)

