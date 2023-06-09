import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys
import datetime
import math



MODE = 'TX2'
#MODE = 'debug'

if MODE == 'TX2' :
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
    signalStr = str(sender) + str(state) + str(power) + str(motion)
    signalStr += str(pwmL) + str(pwmR) + str(ledA) + str(ledB) + str(ledC) + str(ledD)
    try:
        #print("Start writing serial...")
        inputStr = str(signalStr) + str('e')
        if len(inputStr) == 15:
            print("\npy write:",inputStr)
            if MODE == 'TX2':
                ser.write(str.encode(inputStr))  
            time.sleep(0.01)   
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")


# write_Serial(1,2,0,'c',0,0,1,1,1,1)
# time.sleep(2)
write_Serial(1,2,0,'m',0,0,1,1,1,1)
time.sleep(20)
# write_Serial(1,2,0,'r',0,0,1,1,1,1)
# time.sleep(3)
# write_Serial(1,2,0,'k',0,0,1,1,1,1)
# time.sleep(1)
# write_Serial(1,2,0,'s',0,0,1,1,1,1)
# time.sleep(2)
# write_Serial(1,2,0,'l',0,0,1,1,1,1)
# time.sleep(1)
# write_Serial(1,2,0,'k',0,0,1,1,1,1)
# time.sleep(1)
# write_Serial(1,2,0,'s',0,0,1,1,1,1)
# time.sleep(2)


if MODE == 'TX2':
    ser.close()
