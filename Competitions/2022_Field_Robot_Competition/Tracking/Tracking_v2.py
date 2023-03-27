from telnetlib import ECHO
import serial
import time
import util

try:
    COM_PORT = 'COM6'
    ser = serial.Serial(COM_PORT, 9600)
except:
    print("Can not open port:",COM_PORT)
    print("Can not open port:",COM_PORT)
    print("Can not open port:",COM_PORT)


def write_serial(receiver='A',stage=0,state=0,pwm_L=0,pwm_R=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + util.Num2Str(pwm_L) + util.Num2Str(pwm_R)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            #print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")

try:    
    while True:
    
        time.sleep(0.5)

        """ Receive messages """
        while ser.in_waiting:
            #print('serial in waiting')
            write_serial('A',1,0,0,0)

            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            print(str(echoStr))
            
except KeyboardInterrupt:
    ser.close()
    print('bye！')