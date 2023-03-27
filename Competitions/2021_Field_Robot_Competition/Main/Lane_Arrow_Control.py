import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys

MODE = 'TX2'
#MODE = 'debug'

camera_port = 0


if MODE == 'TX2':
    serialCom = '/dev/ttyACM0'
    ser = serial.Serial(serialCom, 9600)

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
            time.sleep(0.05)   
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")



cap = cv2.VideoCapture(camera_port) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)
state = 'READY'
while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        if state == 'READY':
            print("\nstate:",state)
            write_Serial(1,1,0,0,0,0,2,2,2,2)
            time.sleep(1)
            write_Serial(1,1,1,0,80,80,5,5,5,5)
            time.sleep(1)
            write_Serial(1,1,0,0,0,0,2,2,2,2)
            time.sleep(1)
            state = 'FORWARD'
            
        
        if state == 'FORWARD' :
            write_Serial(1,1,1,0,80,80,5,5,5,5)
            
        if state == 'LEFT' :
            write_Serial(1,1,1,0,40,60,6,0,6,0)
            
        if state == 'RIGHT' :
            write_Serial(1,1,1,0,60,40,0,6,0,6)
            
        if state == 'STOP' :
            write_Serial(1,1,1,0,0,0,2,2,2,2)
            
            
        
        
        print("\nCurrent state:",state)
        
        inputStr = input("To 'I' / 'J' / 'L' / 'K':")
        
        if inputStr == "I" :
            state = 'FORWARD'
        if inputStr == "J" :
            state = 'LEFT'
        if inputStr == "L" :
            state = 'RIGHT'
        if inputStr == "K" :
            state = 'STOP'
            
        if inputStr == "[" :
            print("Turn Left !!!")
            write_Serial(1,1,1,'L',0,0,2,2,2,2)
        if inputStr == "]" :
            print("Turn Right !!!")
            write_Serial(1,1,1,'R',0,0,2,2,2,2)
            

            
        time.sleep(0.1)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            write_Serial(1,2,0,0,0,0,2,2,2,2)
            sys.exit()
            break
    else:
        print("Error: no ret")
        break
    
cap.release()
cv2.destroyAllWindows()

if MODE == 'TX2':
    ser.close()
