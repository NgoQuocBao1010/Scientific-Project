from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2
import imutils

sender = imagezmq.ImageSender(connect_to="tcp://localhost:5555")
rpiName = 'Dummy'

dummyImg = cv2.imread('test.png')
resized = imutils.resize(dummyImg, 200)
# cv2.imshow('DEMO', resized)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# time.sleep(2.0)

while True:
    print("Sending")
    sender.send_image(rpiName, resized)
    print('Sended')
