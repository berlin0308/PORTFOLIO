import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import serial



camera_port = 0


TOMATO_threshold = 4500
LEMON_threshold = 4500
AVOCADO_threshold = 4500

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

Hmin_black_phase1 = 10
Smin_black_phase1 = 0
Vmin_black_phase1 = 0
Hmax_black_phase1 = 200
Smax_black_phase1 = 255
Vmax_black_phase1 = 100


def find_tomato(frame,least_area,Hmin_red1,Smin_red1,Vmin_red1,Hmax_red1,Smax_red1,Vmax_red1, Hmin_red2,Smin_red2,Vmin_red2,Hmax_red2,Smax_red2,Vmax_red2):

    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
    
    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
    
    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_black = np.array([Hmin_black, Smin_black, Vmin_black])
    upper_black = np.array([Hmax_black, Smax_black, Vmax_black])
    mask_black = cv2.inRange(cvted_img, lower_black, upper_black)
    #cv2.imshow("black mask", mask_black)
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

while cap.isOpened():  # Capture frame-by-frame
    
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break
    
    ret, frame = cap.read()
    cv2.imshow("original",frame)
    if ret == True:
        frame = cv2.resize(frame, (640, 480))

        x = 200
        y = 250
        w = 150
        h = 100

        polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
        cv2.polylines(frame,pts=[polygon],isClosed=True,color=(90,120,225),thickness=3)

        cv2.imshow("original",frame)

        """ cropping """
        crop = frame[y:y+h, x:x+w]
        #cv2.imshow("cropped",crop)
        tomato_area, TOMATO, frame_tomato = find_tomato(crop,TOMATO_threshold,Hmin_red1_phase1, Smin_red1_phase1, Vmin_red1_phase1, Hmax_red1_phase1, Smax_red1_phase1, Vmax_red1_phase1, Hmin_red2_phase1, Smin_red2_phase1, Vmin_red2_phase1, Hmax_red2_phase1, Smax_red2_phase1, Vmax_red2_phase1)
        print("Tomato:",TOMATO,tomato_area)
        #cv2.imshow("Tomato",frame_tomato)

        lemon_area, LEMON, frame_lemon = find_lemon(crop,LEMON_threshold,Hmin_green_phase1,Smin_green_phase1,Vmin_green_phase1,Hmax_green_phase1,Vmax_green_phase1,Vmax_green_phase1)
        print("Lemon:",LEMON,lemon_area)
        #cv2.imshow("Lemon",frame_lemon)

        avocado_area, AVOCADO, frame_avocado = find_avocado(crop,AVOCADO_threshold,Hmin_black_phase1,Smin_black_phase1,Vmin_black_phase1,Hmax_black_phase1,Vmax_black_phase1,Vmax_black_phase1)
        print("Avocado:",AVOCADO,avocado_area)
        #cv2.imshow("Avocado",frame_avocado)

        crop = cv2.cvtColor(crop,cv2.COLOR_BGR2GRAY)
        Display_Fruits_1 =  cv2.hconcat([crop,frame_tomato])
        Display_Fruits_2 =  cv2.hconcat([frame_lemon,frame_avocado])
        Display_Fruits = cv2.vconcat([Display_Fruits_1,Display_Fruits_2])
        cv2.imshow("crop / tomato \n lemon / avocado",Display_Fruits)
                    
        countFruit = 0
        for fruit in [TOMATO,LEMON,AVOCADO] :
            if fruit == True:
                countFruit += 1

        if countFruit == 0:
            print("No fruit is found...")
        elif countFruit == 1:
            #print("Only 1 is found")
            if TOMATO == True:
                print("\nOnly TOMATO is found")
            if LEMON == True:
                print("\nOnly LEMON is found")
            if AVOCADO == True:
                print("\nOnly AVOCADO is found")
        elif countFruit == 2:
            print("\n2 are found")
        elif countFruit == 3:
            print("\n3 are found")
            
        
        time.sleep(0.4)
        
    else:
        print("Error: no ret")
        break


cap.release()
cv2.destroyAllWindows()
