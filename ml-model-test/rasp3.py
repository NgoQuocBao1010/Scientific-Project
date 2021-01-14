import cv2
import datetime
import base64
import time


MAXIMUM_NUMBER_OF_SEND_FRAMES = 20
LIST_OF_FRAMES = []


cap = cv2.VideoCapture(0)
time.sleep(2)
i = -1
while True:
    if cv2.waitKey(25) == 13:
        break

    ret, frame = cap.read()
    i += 1
    if i % 2 != 0:
        continue

    cv2.imshow('DEMO', frame)

