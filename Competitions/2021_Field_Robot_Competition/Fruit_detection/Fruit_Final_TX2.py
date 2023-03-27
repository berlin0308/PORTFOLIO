import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys


MODE = 'TX2'
MODE = 'debug'

camera_port = 0

READY_delay = 3

FORWARD_1_delay = 3
FORWARD_1_pwm = 60

SLOWDOWN_1_pwm = 20

STOP_1_delay = 5

GRAB_delay = 6

FORWARD_2_delay = 5
FORWARD_2_pwm = 60

STOP_1_delay = 5

SLOWDOWN_2_pwm = 20

STOP_2_delay = 5

FORWARD_3_pwm = 40

STOP_3_delay = 10

PAUSE_delay = 2


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

if MODE == 'TX2':
    serialCom = '/dev/ttyACM0'
    ser = serial.Serial(serialCom, 9600)

def MOTION_STATE_PWM(MOTION_STATE):
    pwmL, pwmR = 0,0
    if MOTION_STATE == 'READY':
        pwmL, pwmR = 0,0
        
    if MOTION_STATE == 'FORWARD_1':
        pwmL, pwmR = FORWARD_1_pwm,FORWARD_1_pwm
    
    if MOTION_STATE == 'SLOWDOWN_1':
        pwmL, pwmR = SLOWDOWN_1_pwm,SLOWDOWN_1_pwm
        
    if MOTION_STATE == 'STOP_1':
        pwmL, pwmR = 0,0
    
    if MOTION_STATE == 'GRAB':
        pwmL, pwmR = 0,0
    
    if MOTION_STATE == 'FORWARD_2':
        pwmL, pwmR = FORWARD_2_pwm,FORWARD_2_pwm
        
    if MOTION_STATE == 'SLOWDOWN_2':
        pwmL, pwmR = SLOWDOWN_2_pwm,SLOWDOWN_2_pwm
        
    if MOTION_STATE == 'STOP_2':
        pwmL, pwmR = 0,0
        
    if MOTION_STATE == 'FORWARD_3':
        pwmL, pwmR = FORWARD_3_pwm,FORWARD_3_pwm
    
    if MOTION_STATE == 'STOP_3':
        pwmL, pwmR = 0,0
        
    return pwmL, pwmR
    

def MOTION_STATE_LEDs(MOTION_STATE):
    A,B,C,D = 1,1,1,1
    
    if MOTION_STATE == 'TOMATO':
        A,B,C,D = 2,2,2,2  # Red
    
    if MOTION_STATE == 'LEMON':
        A,B,C,D = 3,3,3,3  # Green
    
    if MOTION_STATE == 'AVOCADO':
        A,B,C,D = 4,4,4,4  # Blue
    
    
    if MOTION_STATE == 'READY':
        A,B,C,D = 7,7,7,7  # Megenta
        
    if MOTION_STATE == 'FORWARD_1':
        A,B,C,D = 5,5,5,5  # Cyan
        
    if MOTION_STATE == 'SLOWDOWN_1':
        A,B,C,D = 6,6,6,6  # YELLOW
    
    if MOTION_STATE == 'STOP_1':
        A,B,C,D = 7,7,7,7  # Megenta
        
    if MOTION_STATE == 'GRAB':
        A,B,C,D = 1,1,1,1  # White
            
    if MOTION_STATE == 'FORWARD_2':
        A,B,C,D = 5,5,5,5  # Cyan
        
    if MOTION_STATE == 'SLOWDOWN_2':
        A,B,C,D = 6,6,6,6  # YELLOW
    
    if MOTION_STATE == 'STOP_2':
        A,B,C,D = 7,7,7,7  # Megenta
    
    if MOTION_STATE == 'FORWARD_3':
        A,B,C,D = 5,5,5,5  # Cyan
        
    if MOTION_STATE == 'STOP_3':
        A,B,C,D = 7,7,7,7  # Megenta
        
    print("A B   ",A,B)
    print("C D   ",C,D)
    return A,B,C,D


def Num2Str(num):
    if str(type(num)) == "<class 'int'>":
        converted = str(num)
        if len(converted) > 3:
            print("Error: invalid num length\nlen:",len(converted))
            return "!!!"
        if len(converted) == 1:
            converted = "00" + converted
        if len(converted) == 2:
            converted = "0" + converted
        return str(converted)
    else:
        print("Error: not int\ndatatype:",type(num))
        return "!!!"

def write_Serial(sender=0,state=0,power=0,motion=0,pwmL=0,pwmR=0,ledA=0,ledB=0,ledC=0,ledD=0):
    pwmL = Num2Str(pwmL)
    pwmR = Num2Str(pwmR)
    print("pwmL:",pwmL)
    print("pwmR:",pwmR)
    signalStr = str(sender) + str(state) + str(power) + str(motion)
    signalStr += str(pwmL) + str(pwmR) + str(ledA) + str(ledB) + str(ledC) + str(ledD)
    try:
        #print("Start writing serial...")
        inputStr = str(signalStr) + str('e')
        if len(inputStr) == 15:
            print("py write:",inputStr)
            if MODE == 'TX2':
                ser.write(str.encode(inputStr))  
            time.sleep(0.01)
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")

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


def find_Fruit(frame):

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
        return "void"
    elif countFruit == 1:
        #print("Only 1 is found")
        if TOMATO == True:
            print("\nOnly TOMATO is found")
            return "TOMATO"
        if LEMON == True:
            print("\nOnly LEMON is found")
            return "LEMON"
        if AVOCADO == True:
            print("\nOnly AVOCADO is found")
            return "AVOCADO"
    elif countFruit == 2:
        print("\n2 are found")
        return "void"
    elif countFruit == 3:
        print("\n3 are found")
        return "void"

def find_box(frame):
    return "NOBOX"
 
def Fruit_to_Box(fruit):
    if fruit == "TOMATO":
        return "REDBOX"
    if fruit == "LEMON":
        return "GREENBOX"
    if fruit == "AVOCADO":
        return "BLUEBOX"

def grab_Fruit():    # to be determined
    write_Serial(1,2,0,'c',0,0,1,1,1,1)
    time.sleep(2)
    write_Serial(1,2,0,'m',0,0,1,1,1,1)
    time.sleep(2)
    write_Serial(1,2,0,'s',0,0,1,1,1,1)
    time.sleep(2)
    
def drop_Fruit():
    write_Serial(1,2,0,'l',0,0,1,1,1,1)
    time.sleep(2)
    write_Serial(1,2,0,'r',0,0,1,1,1,1)
    time.sleep(2)


cap = cv2.VideoCapture(camera_port) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)
state = 'READY'
Fruit = "void"
while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()
    pwmL, pwmR = 0, 0
    if ret == True:
        if state == 'READY':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,0,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            time.sleep(READY_delay)
            state = 'FORWARD_1'
            time.sleep(PAUSE_delay)
            
        if state == 'FORWARD_1':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            time.sleep(FORWARD_1_delay)
            state = 'SLOWDOWN_1'
            time.sleep(PAUSE_delay)

        if state == 'SLOWDOWN_1':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            Fruit = find_Fruit(frame)
            print("Fruit found:",Fruit)
            if Fruit != "void":
                state = 'STOP_1'
                time.sleep(PAUSE_delay)
       

        if state == 'STOP_1':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(Fruit) # R,G,B for TOMATO,LEMON,AVOCADO
            write_Serial(1,2,0,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            time.sleep(STOP_1_delay)
            state = "GRAB"
            time.sleep(PAUSE_delay)
            
        
        if state == "GRAB":
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,0,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            print("Start GRABBING Fruit...")
            grab_Fruit()
            print("Fruit GRABBED!")
            
            time.sleep(GRAB_delay)
            state = "FORWARD_2"
            time.sleep(PAUSE_delay)
            
        
        if state == 'FORWARD_2':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            time.sleep(FORWARD_2_delay)
            state = 'SLOWDOWN_2'
            time.sleep(PAUSE_delay)

        if state == 'SLOWDOWN_2':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            Box = find_box(frame)
            if Box != "void":
                if Box == Fruit_to_Box(Fruit):
                    print("Box found:",Box)
                    state = 'STOP_2'  
                    time.sleep(PAUSE_delay)
                else:
                    pass                
        
        if state == 'STOP_2':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            write_Serial(1,2,0,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            print("Start DROPPING Fruit...")
            drop_Fruit()
            print("Fruit DROPPED!")
            time.sleep(STOP_2_delay)
            state = 'FORWARD_3'
            time.sleep(PAUSE_delay)
            
        if state == 'FORWARD_3':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(state)
            write_Serial(1,2,1,'E',pwmL,pwmR,ledA,ledB,ledC,ledD) # stop as distanceF less than ?
            time.sleep(20)
            state = 'STOP_3'
        
        if state == 'STOP_3':
            print("\nstate:",state)
            pwmL,pwmR = MOTION_STATE_PWM(state)
            write_Serial(1,2,0,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
            time.sleep(STOP_3_delay)
            state = 'END'
            
        if state == 'END':
            print("\nstate:",state)
            write_Serial(1,2,0,0,0,0,0,0,0,0)
            break
            
            
        time.sleep(0.4)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            sys.exit()
            break
    else:
        print("Error: no ret")
        break
    
cap.release()
cv2.destroyAllWindows()

if MODE == 'TX2':
   ser.close()
