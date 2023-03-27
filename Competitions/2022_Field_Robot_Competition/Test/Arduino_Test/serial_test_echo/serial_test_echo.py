import serial
import time
import sys

COM_PORT = 'COM7'
ser = serial.Serial(COM_PORT, 9600)

try:
    while True:
        inputStr = input('Input:')
        if inputStr != '1':
            print("py input:",inputStr)
            ser.write(str.encode(inputStr))  
            time.sleep(0.5)  
        elif inputStr == '1':
            ser.close()
            print('bye！')
            sys.exit()
            
        time.sleep(1)
        while ser.in_waiting:
            print('serial in waiting')
            echoStr = ser.readline().decode()
            print('arduino:', echoStr)
            
except KeyboardInterrupt:
    ser.close()
    print('bye！')