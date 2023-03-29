import cv2
import numpy as np


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
            if cv2.contourArea(c) < 2500:
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

    if_motion, img_result = check_if_motion(frame)

    cv2.imshow('result', img_result)

cap.release()
cv2.destroyAllWindows()


