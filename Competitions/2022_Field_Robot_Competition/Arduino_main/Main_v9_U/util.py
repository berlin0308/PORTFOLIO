import re
import cv2
import numpy as np


def Num2Str(num):
    if str(type(num)) == "<class 'int'>":
        cvt = str(num)
        if len(cvt) ==2:
            cvt = "0" + cvt
        if len(cvt) ==1:
            cvt = "00" + cvt

        return str(cvt)
    else:
        return "error"


def u_road(frame):
    pwm = ('100', '120')
    middle = 260
    pipe_lower = np.array([0,102,133])   
    pipe_upper = np.array([20,255,255]) 

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (15, 15), 0)
    hsv = hsv[0:,520:]

    pipe_mask = cv2.inRange(hsv, pipe_lower, pipe_upper) 
    pipe_mask = cv2.erode(pipe_mask, None, iterations=2)
    pipe_mask = cv2.dilate(pipe_mask, None, iterations=2)

    pipe_contours, pipe_hierarchy= cv2.findContours(pipe_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(pipe_contours) > 0:
        pipe_cnt = max(pipe_contours, key=cv2.contourArea)
        pipe_output = cv2.bitwise_and(hsv, hsv, mask = pipe_mask)

        M = cv2.moments(pipe_cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(pipe_output, (cX, cY), 1, (255, 255, 255), 4)
        cv2.imshow('pipe', pipe_output)

        if cY > middle+1:
            #turn left
            pwm = ('045', '125')
            print('turn left')
            return pwm
        elif cY < middle-1:
            #turn right
            pwm = ('120','050')
            print('turn right')
            return pwm
            
    return pwm


# cap = cv2.VideoCapture(1)

# while True:
#     ret, frame = cap.read()
#     color, output = color_sign_recog(frame)
#     cv2.imshow("find sign",output)
#     if cv2.waitKey(1) == ord('Q'):
#         break
#     print(color)  
    
# cv2.waitKey()
# cap.release()
# cv2.destroyAllWindows()
  