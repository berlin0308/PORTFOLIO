import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys

camera_port = 0

READY_delay = 5

FORWARD_1_delay = 5
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

PAUSE_delay = 5

# serialCom = '/dev/ttyACM0'
# ser = serial.Serial(serialCom, 9600)

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
            #ser.write(str.encode(inputStr))  
            time.sleep(1)   
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")


def find_fruit(frame):
    return "TOMATO"

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
            Fruit = find_fruit(frame)
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
            
            
        time.sleep(0.1)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            sys.exit()
            break
    else:
        print("Error: no ret")
        break
    
cap.release()
cv2.destroyAllWindows()

#ser.close()
