from imutils.video import VideoStream
import imagezmq
import argparse
import socket
import time
import cv2
import imutils

sender = imagezmq.ImageSender(connect_to="tcp://localhost:5555")

rpiName = socket.gethostname()
print(rpiName)
# vs = cv2.VideoCapture(0)
vs = VideoStream(src=0, resolution=(320, 240)).start()
time.sleep(2.0)

while True:
    print("Sending")
    frame = vs.read()
    frame = imutils.resize(frame, 320)
    sender.send_image(rpiName, frame)
    print('Sended')
