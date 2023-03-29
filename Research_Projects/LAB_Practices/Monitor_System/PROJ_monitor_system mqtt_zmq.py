import imp
import cv2
import numpy as np
import os
import sys
import datetime
import time
import paho.mqtt.client as mqtt
import imagezmq
import json

def check_if_motion(img):
        global avg
        motionDetected = False
  #  try:
        blur = cv2.blur(img, (4, 4))
        diff = cv2.absdiff(avg, blur)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            if cv2.contourArea(c) < 4000:
                continue
            motionDetected = True
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.drawContours(img, cnts, -1, (0, 255, 255), 2)
        cv2.accumulateWeighted(blur, avg_float, 0.01)
        avg = cv2.convertScaleAbs(avg_float)
    #except:
        #print("Exception")
        return motionDetected,img 


def check_if_face(img):

    faceDetected = False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 10)
    for (x, y, w, h) in faces:
        faceDetected = True
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)


    return faceDetected,img



face_cascade = cv2.CascadeClassifier(sys.path[0]+"\\haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)

width = 1080
height = 720

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

    if_face, img_marked = check_if_face(frame)
    if_motion, img_marked = check_if_motion(img_marked)

    current_time = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    payload = {"ID": "B09611007", "Name": "Berlin", "Time": current_time
                ,"motion":str(if_motion),"face":str(if_face)}

    img_display = cv2.resize(img_marked,(540,360))
    img_display = cv2.putText(img_display,current_time,(10,346)
                              ,cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow('monitor', img_display)

    if if_face or if_motion:
        try:
            client = mqtt.Client(client_id="berlin")
            client.username_pw_set('chen', '0000')
            client.connect('140.112.94.129', 20010, 60)

            """ MQTT """
            client.publish("mqtt_class/test", json.dumps(payload))
            print(payload)

            """ imageZMQ """
            sender = imagezmq.ImageSender(connect_to='tcp://140.112.94.129:20009')
            sender.send_image("Berlin", img_marked)

            time.sleep(20)
        except:
            print("Exception")


cap.release()
cv2.destroyAllWindows()


