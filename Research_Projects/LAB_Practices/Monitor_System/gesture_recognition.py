import cv2
import numpy as np
import os
import sys


def check_if_face(img):

    faceDetected = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        faceDetected = True
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)


    return faceDetected,img


print(sys.path[0])
face_cascade = cv2.CascadeClassifier(sys.path[0]+"\\haarcascade_fullbody.xml")
cap = cv2.VideoCapture(0)

width = 1280
height = 960

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

area = width * height

ret, frame = cap.read()
avg = cv2.blur(frame, (4, 4))
avg_float = np.float32(avg)

while(cap.isOpened()):

    ret, frame = cap.read()
    #cv2.imshow('frame', frame);
    if ret == False:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if_face, img_result = check_if_face(frame)
    cv2.imshow('result', img_result)

cap.release()
cv2.destroyAllWindows()


