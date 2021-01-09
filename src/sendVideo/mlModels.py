import numpy as np
import cv2
import os
# from mtcnn.mtcnn import MTCNN

# resize image by giving the size in tuple: (new width, new height)
def resizeImage(image, coordinate=(0, 0)):
    try:
        width, height = coordinate
        image = cv2.resize(image, (width, height))
        return image
    except Exception as e:
        # print(str(e))
        return None

# transform image to black and white
def grayscaleImage(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray
    except Exception as e:
        # print(str(e))
        return None


def usingDeepLearning2(picPath, savedPath):
    pic = cv2.imread(picPath)
    net = cv2.dnn.readNetFromCaffe("deploy.prototxt.txt", "res10_300x300_ssd_iter_140000.caffemodel")
    
    blob = cv2.dnn.blobFromImage(cv2.resize(pic, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    (h, w) = pic.shape[:2]

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence < 0.4:
            continue

        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        
        try:
            pic = pic[startY:endY, startX:endX]
            pic = grayscaleImage(pic)
            pic = resizeImage(pic, (100, 100))
            cv2.imwrite(savedPath, pic)
        except:
            continue




# usingDeepLearning2('myself.jpg')