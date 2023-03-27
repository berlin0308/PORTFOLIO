import serial
import time
import sys


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
        print("Start writing serial...")
        inputStr = str(signalStr) + str('e')
        if len(inputStr) == 15:
            print("py write:",inputStr)
            ser.write(str.encode(inputStr))  
            time.sleep(1)   
        else:
            print("Error: serial inputStr length:",len(inputStr))
           
    except KeyboardInterrupt:
        ser.close()
        print("keyboard interrupted!")
   
   
""" observe motor speed, LED """
pwmL = int(input("pwmL:"))
pwmR = int(input("pwmR:"))
count = 0
while True:
    write_Serial(1,1,1,0,pwmL,pwmR,count%8,1,1,1)
    count += 1
    while ser.in_waiting:
        echoStr = ser.readline().decode()
        print('arduino:', echoStr)
        

ser.close()
