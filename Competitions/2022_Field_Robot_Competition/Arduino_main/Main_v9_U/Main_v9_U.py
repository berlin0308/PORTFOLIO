from telnetlib import ECHO
from unittest import result
import serial
import time
import sys
import util
import cv2


COM_PORT = 'COM6'
ser = serial.Serial(COM_PORT, 9600)
STAGE = 7
STATE = 1
pwmL = 0
pwmR = 0
frontCamLED = 0
sideCamLED = 0
Stepper = 0
Pump = 0


def write_serial(receiver='A',stage=0,state=0,pwm_L=0,pwm_R=0,fCam=0,sCam=0,stepper=0,pump=0):
    Py_input = str(receiver) + str(stage) + str(state) + util.Num2Str(pwm_L) + util.Num2Str(pwm_R)
    Py_input += str(fCam) + str(sCam) + str(stepper) + str(pump) + str("e")
    try:
        if len(Py_input) == 14:
            print("From py:",Py_input)
            ser.write(str.encode(Py_input))
    except:
        print("\n\nwrite serial error\n\n")


SIGN_COLOR = 'null'

try:
    frontCam = cv2.VideoCapture(0)
    sideCam = cv2.VideoCapture(1)
    
    while True:

        time.sleep(1)

        print("\nSTAGE:",STAGE)
        print("STATE:",STATE)

        """ For each STAGE, STATE """
        if STAGE == 0: #STOP
            pass
        
            
        if STAGE == 3: #N3
            write_serial('A',3,1)
        if STAGE == 4: #T1
            pass
        if STAGE == 5: #T2
            pass
        if STAGE == 6: #T3
            pass
        
        if STAGE == 7: #U
            ret, frame = sideCam.read()
            #try:
            PWM = util.u_road(frame)
            ser.write(str.encode("A70"+PWM[0]+PWM[1]+"0000e"))
        #except

        """ Receive messages """
        while ser.in_waiting:
            time.sleep(0.4)
            #print('serial in waiting')
            echoStr = str(ser.readline().decode()).strip(' ').strip('\n')
            #print(str(echoStr))
            
            try:
                Receiver = echoStr[0]
                if_STAGE_changed = echoStr[1]
                STAGE_changed = echoStr[2]
                if_STATE_changed = echoStr[3]
                STATE_changed = echoStr[4]
                
                if Receiver=='P': # Arduino -> Python 
                    print('From arduino:', echoStr)
                    if if_STAGE_changed == '1': # button pressed, STAGE changed
                        #print("Change stage to:",STAGE_changed)
                        STAGE = int(STAGE_changed)
                        #STATE = 0
                    if if_STATE_changed == '1': # STATE changed
                        #print("Change state to:",STATE_changed)
                        STATE = int(STATE_changed)

                if Receiver=='D': # Arduino debug messages
                    print("\n-----")
                    print("From debug:",echoStr[2:])
                    print("-----\n")
            except:
                pass
                        
        """ Write messages to Arduino""" 
        #print("start writing serial...")
        #write_serial('A',STAGE,STATE,pwmL,pwmR,frontCamLED,sideCamLED,Stepper,Pump)

    cv2.waitKey()
    sideCam.release()
    cv2.destroyAllWindows()
    
except KeyboardInterrupt:
    ser.close()
    print('bye！')





