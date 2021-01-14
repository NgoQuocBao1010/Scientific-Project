# Import the necessary packages
import datetime as dt
from EAR_calculator import *
from imutils import face_utils
from matplotlib import style
import imutils
import dlib
import time
import cv2
import base64
import numpy as np

# parameter
distracton_initlized = False
eye_initialized = False
mouth_initialized = False

EAR_THRESHOLD = 0.1

MAR_THRESHOLD = 12

CONSECUTIVE_FRAMES = 5

model_path = 'shape_predictor_68_face_landmarks.dat'

# Now, intialize the dlib's face detector model as 'detector' and the landmark predictor model as 'predictor'
print("[INFO]Loading the predictor.....")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(model_path)

# Grab the indexes of the facial landamarks for the left and right eye respectively
(lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

count_sleep = 0
count_yawn = 0

def convertStrByteToImg(strByte):
    im_b64 = str.encode(strByte)
    f = base64.b64decode(im_b64)
    im_arr = np.frombuffer(f, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)

    return img


def detectionDrowsiness(frames):
    # Initialize two counters
    BLINK_COUNT = 0
    FRAME_COUNT_EAR = 0
    FRAME_COUNT_MAR = 0
    FRAME_COUNT_DISTR = 0

    # Now, loop over all the frames and detect the faces
    for frame in frames:
        frame = convertStrByteToImg(frame)
        cv2.putText(frame, "PRESS 'q' TO EXIT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)

        # Resize the frame
        frame = imutils.resize(frame, width=500)

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        rects = detector(frame, 1)

        # Now loop over all the face detections and apply the predictor
        if rects is not None:
            rect = get_max_area_rect(rects)

            if rect is not None:
                shape = predictor(gray, rect)
                # Convert it to a (68, 2) size numpy array
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[lstart:lend]
                rightEye = shape[rstart:rend]
                mouth = shape[mstart:mend]

                # Compute the EAR for both the eyes
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # Take the average of both the EAR
                EAR = (leftEAR + rightEAR) / 2.0

                # Compute the convex hull for both the eyes and then visualize it
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)

                # Draw the contours
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [mouth], -1, (0, 255, 0), 1)

                MAR = mouth_aspect_ratio(mouth)

                # Check if EAR < EAR_THRESHOLD, if so then it indicates that a blink is taking place
                # Thus, count the number of frames for which the eye remains closed
                if EAR < EAR_THRESHOLD:
                    FRAME_COUNT_EAR += 1

                    cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
                    cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

                    if FRAME_COUNT_EAR >= CONSECUTIVE_FRAMES:
                        # Add the frame to the dataset ar a proof of drowsy driving
                        cv2.putText(frame, "DROWSINESS ALERT!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    FRAME_COUNT_EAR = 0

                # Check if the person is yawning
                if MAR > MAR_THRESHOLD:
                    FRAME_COUNT_MAR += 1

                    cv2.drawContours(frame, [mouth], -1, (0, 0, 255), 1)

                    if FRAME_COUNT_MAR >= 5:
                        print('yawning')
                        cv2.putText(frame, "YOU ARE YAWNING!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    FRAME_COUNT_MAR = 0

        else:
            FRAME_COUNT_DISTR += 1

            if FRAME_COUNT_DISTR >= CONSECUTIVE_FRAMES:
                print('EYES ON ROAD PLEASE!!!')
                cv2.putText(frame, "EYES ON ROAD PLEASE!!!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                FRAME_COUNT_DISTR = 0

        cv2.imshow("DEMO", frame)
