# # Import the necessary packages
# import datetime as dt
# from EAR_calculator import *
# from imutils import face_utils
# from matplotlib import style
# import imutils
# import dlib
# import time
# import cv2

# # parameter
# distracton_initlized = False
# eye_initialized = False
# mouth_initialized = False

# EAR_THRESHOLD = 0.2

# MAR_THRESHOLD = 10

# CONSECUTIVE_FRAMES = 20

# model_path = 'shape_predictor_68_face_landmarks.dat'

# # Initialize two counters
# BLINK_COUNT = 0
# FRAME_COUNT_EAR = 0
# FRAME_COUNT_MAR = 0
# FRAME_COUNT_DISTR = 0

# # Now, intialize the dlib's face detector model as 'detector' and the landmark predictor model as 'predictor'
# print("[INFO]Loading the predictor.....")
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor(model_path)

# # Grab the indexes of the facial landamarks for the left and right eye respectively
# (lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# (rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
# (mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# # Now start the video stream and allow the camera to warm-up
# print("[INFO]Loading Camera.....")
# video_capture = cv2.VideoCapture('5182892353891652053.mp4')
# time.sleep(2)

# count_sleep = 0
# count_yawn = 0

# # Now, loop over all the frames and detect the faces
# while True:
#     # Extract a frame
#     _, frame = video_capture.read()
#     cv2.putText(frame, "PRESS 'q' TO EXIT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)

#     # Resize the frame
#     frame = imutils.resize(frame, width=500)

#     # Convert the frame to grayscale
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Detect faces
#     rects = detector(frame, 1)

#     # Now loop over all the face detections and apply the predictor
#     if rects is not None:
#         rect = get_max_area_rect(rects)
#         shape = predictor(gray, rect)
#         # Convert it to a (68, 2) size numpy array
#         shape = face_utils.shape_to_np(shape)

#         leftEye = shape[lstart:lend]
#         rightEye = shape[rstart:rend]
#         mouth = shape[mstart:mend]

#         # Compute the EAR for both the eyes
#         leftEAR = eye_aspect_ratio(leftEye)
#         rightEAR = eye_aspect_ratio(rightEye)

#         # Take the average of both the EAR
#         EAR = (leftEAR + rightEAR) / 2.0

#         # Compute the convex hull for both the eyes and then visualize it
#         leftEyeHull = cv2.convexHull(leftEye)
#         rightEyeHull = cv2.convexHull(rightEye)

#         # Draw the contours
#         cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
#         cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
#         cv2.drawContours(frame, [mouth], -1, (0, 255, 0), 1)

#         MAR = mouth_aspect_ratio(mouth)

#         # Check if EAR < EAR_THRESHOLD, if so then it indicates that a blink is taking place
#         # Thus, count the number of frames for which the eye remains closed
#         if EAR < EAR_THRESHOLD:
#             FRAME_COUNT_EAR += 1

#             cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
#             cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)

#             if FRAME_COUNT_EAR >= CONSECUTIVE_FRAMES:
#                 # Add the frame to the dataset ar a proof of drowsy driving
#                 cv2.putText(frame, "DROWSINESS ALERT!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#         else:
#             FRAME_COUNT_EAR = 0

#         # Check if the person is yawning
#         if MAR > MAR_THRESHOLD:
#             FRAME_COUNT_MAR += 1

#             cv2.drawContours(frame, [mouth], -1, (0, 0, 255), 1)

#             if FRAME_COUNT_MAR >= 10:
#                 cv2.putText(frame, "YOU ARE YAWNING!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#             else:
#                 FRAME_COUNT_MAR = 0
#     else:
#         FRAME_COUNT_DISTR += 1

#         if FRAME_COUNT_DISTR >= CONSECUTIVE_FRAMES:
#             cv2.putText(frame, "EYES ON ROAD PLEASE!!!", (270, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#         else:
#             FRAME_COUNT_DISTR = 0

#     cv2.imshow("DEMO", frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord("q"):
#         break

