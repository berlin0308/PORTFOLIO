import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import serial



camera_port = 1

path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\findfruit7.jpg"

H_ideal_green = 60
S_ideal_green = 255
V_ideal_green = 150

Hmin_green_phase1 = 35
Smin_green_phase1 = 70
Vmin_green_phase1 = 30
Hmax_green_phase1 = 80
Smax_green_phase1 = 255
Vmax_green_phase1 = 255

Hmin_red1_phase1 = 0
Smin_red1_phase1 = 50
Vmin_red1_phase1 = 20
Hmax_red1_phase1 = 10
Smax_red1_phase1 = 255
Vmax_red1_phase1 = 255

Hmin_red2_phase1 = 175
Smin_red2_phase1 = 50
Vmin_red2_phase1 = 20
Hmax_red2_phase1 = 180
Smax_red2_phase1 = 255
Vmax_red2_phase1 = 255

Hmin_black_phase1 = 0
Smin_black_phase1 = 0
Vmin_black_phase1 = 0
Hmax_black_phase1 = 200
Smax_black_phase1 = 255
Vmax_black_phase1 = 100


Guassian_ksize = 45
morphol_kernel = 20

"""
Approach1
鏡頭逼近水果 看小範圍
從最寬的HSV range標準檢查是否有水果
若有則縮小範圍
(適合後面有背景
"""

def find_tomato(frame,least_area,Hmin_red1,Smin_red1,Vmin_red1,Hmax_red1,Smax_red1,Vmax_red1, Hmin_red2,Smin_red2,Vmin_red2,Hmax_red2,Smax_red2,Vmax_red2):

    """ cropping """
    frame = cv2.resize(frame, (640, 480))
    x = 240
    y = 180
    w = 160
    h = 120
    cropped = frame[y:y+h, x:x+w]
    #cv2.imshow("cropped",cropped)
    
    """ thresholding """
    cvted_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_red1 = np.array([Hmin_red1, Smin_red1, Vmin_red1])
    upper_red1 = np.array([Hmax_red1, Smax_red1, Vmax_red1])
    mask_red1 = cv2.inRange(cvted_img, lower_red1, upper_red1)
    #cv2.imshow("red1 mask", mask_red1)
    lower_red2 = np.array([Hmin_red2, Smin_red2, Vmin_red2])
    upper_red2 = np.array([Hmax_red2, Smax_red2, Vmax_red2])
    mask_red2 = cv2.inRange(cvted_img, lower_red2, upper_red2)
    #cv2.imshow("red2 mask", mask_red2)

    mask_red = cv2.bitwise_or(mask_red1,mask_red2)
    #cv2.imshow("mask_red", mask_red)
    frame_tomato = mask_red
    
    """ calculate area """
    Area = cv2.countNonZero(frame_tomato)
    
    if Area > least_area:
        return Area, True, frame_tomato
    else:
        return Area, False, frame_tomato

def find_lemon(frame,least_area,Hmin_green,Smin_green,Vmin_green,Hmax_green,Smax_green,Vmax_green):

    """ cropping """
    frame = cv2.resize(frame, (640, 480))
    x = 240
    y = 180
    w = 160
    h = 120
    cropped = frame[y:y+h, x:x+w]
    #cv2.imshow("cropped",cropped)
    
    """ thresholding """
    cvted_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([Hmin_green, Smin_green, Vmin_green])
    upper_green = np.array([Hmax_green, Smax_green, Vmax_green])
    mask_green = cv2.inRange(cvted_img, lower_green, upper_green)
    #cv2.imshow("green mask", mask_green)
    frame_lemon = mask_green
    
    """ calculate area """
    Area = cv2.countNonZero(mask_green)
    
    if Area > least_area:
        return Area, True, frame_lemon
    else:
        return Area, False, frame_lemon

def find_avocado(frame,least_area,Hmin_black,Smin_black,Vmin_black,Hmax_black,Smax_black,Vmax_black):

    """ cropping """
    frame = cv2.resize(frame, (640, 480))
    x = 240
    y = 180
    w = 160
    h = 120
    cropped = frame[y:y+h, x:x+w]
    cv2.imshow("cropped",cropped)
    
    """ thresholding """
    cvted_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_black = np.array([Hmin_black, Smin_black, Vmin_black])
    upper_black = np.array([Hmax_black, Smax_black, Vmax_black])
    mask_black = cv2.inRange(cvted_img, lower_black, upper_black)
    cv2.imshow("black mask", mask_black)
    frame_avocado = mask_black
    
    """ calculate area """
    Area = cv2.countNonZero(mask_black)
    
    if Area > least_area:
        return Area, True, frame_avocado
    else:
        return Area, False, frame_avocado




cap = cv2.VideoCapture(camera_port) 
#cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)
#cap = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW)

if camera_port == 0:   # notebook camera
    #cap.set(cv2.CAP_PROP_EXPOSURE,-4)
    #cap.set(cv2.CAP_PROP_CONTRAST,0)
    print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))
    
if camera_port == 1:  # usb camera
    cap.set(cv2.CAP_PROP_EXPOSURE,-7)
    cap.set(cv2.CAP_PROP_CONTRAST,10)
    print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))

print("Start capturing video from the camera")

if cap.isOpened() == False:
    print("Error: Failed to read the video stream")
else:
    print("Read images successfully\n")
 
countImage = 0
while cap.isOpened():  # Capture frame-by-frame
    try:
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break
        ret, frame = cap.read()
        if countImage == 1:
            print("height:",frame.shape[0],"width:",frame.shape[1],"channel:",frame.shape[2])
            print("Image type:",type(frame))
            
        #print("\ncount:",countImage,'\n')
        cv2.imshow("original",frame)
        if ret == True:
            tomato_area, TOMATO, frame_tomato = find_tomato(frame,6000,Hmin_red1_phase1, Smin_red1_phase1, Vmin_red1_phase1, Hmax_red1_phase1, Smax_red1_phase1, Vmax_red1_phase1, Hmin_red2_phase1, Smin_red2_phase1, Vmin_red2_phase1, Hmax_red2_phase1, Smax_red2_phase1, Vmax_red2_phase1)
            print('\n',tomato_area,TOMATO)

            lemon_area, LEMON, frame_lemon = find_lemon(frame,6500,Hmin_green_phase1,Smin_green_phase1,Vmin_green_phase1,Hmax_green_phase1,Vmax_green_phase1,Vmax_green_phase1)
            print(lemon_area, LEMON)
            #cv2.imshow("lemon",frame_lemon)
            
            avocado_area, AVOCADO, frame_avocado = find_avocado(frame,6500,Hmin_black_phase1,Smin_black_phase1,Vmin_black_phase1,Hmax_black_phase1,Vmax_black_phase1,Vmax_black_phase1)
            print(avocado_area, AVOCADO,'\n')
            
                        
            countFruit = 0
            for fruit in [TOMATO,LEMON,AVOCADO] :
                if fruit == True:
                    countFruit += 1

            if countFruit == 0:
                print("No fruit is found...")
            elif countFruit == 1:
                print("Only 1 is found")
                if TOMATO == True:
                    print("Only TOMATO is found")
                if LEMON == True:
                    print("Only LEMON is found")
                if AVOCADO == True:
                    print("Only AVOCADO is found")
            elif countFruit == 2:
                print("2 are found")
            elif countFruit == 3:
                print("3 are found")
                
                
            display = cv2.vconcat([frame_tomato,frame_lemon]) 
            display = cv2.vconcat([display,frame_avocado]) 
            cv2.imshow("display",display)
            
            time.sleep(0.2)
            
            countImage += 1
        else:
            print("Error: no ret")
            break
    except :
        print("Error: Failed to capture the video")
        time.sleep(0.02)
   
    
cap.release()
cv2.destroyAllWindows()
