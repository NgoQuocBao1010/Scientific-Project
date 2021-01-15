import numpy as np
import cv2
import os
import base64
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


def convertStrByteToImg(strByte):
    try:
        im_b64 = str.encode(strByte)
        f = base64.b64decode(im_b64)
        im_arr = np.frombuffer(f, dtype=np.uint8)
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

        return img
    except Exception as e:
        # print(str(e))
        return None


def usingDeepLearning2(picStrBytes):
    pic = convertStrByteToImg(picStrBytes)

    if pic is None:
        return None

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
            # pic = pic[startY:endY, startX:endX]
            pic = grayscaleImage(pic)
            cv2.rectangle(pic, (startX, startY), (endX, endY), (255, 0, 0), 2)
            pic = resizeImage(pic, (400, 400))
            _, im_arr = cv2.imencode('.jpg', pic)
            im_bytes = im_arr.tobytes()
            im_b64 = base64.b64encode(im_bytes)
            im_data_str = im_b64.decode('utf-8')
            return im_data_str
        except:
            return None
    




# usingDeepLearning2('myself.jpg')