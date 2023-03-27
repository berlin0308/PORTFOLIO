import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys

serialCom = '/dev/ttyACM0'
ser = serial.Serial(serialCom, 9600)

def MOTION_STATE_LEDs(MOTION_STATE):
    A,B,C,D = 1,1,0,0
    if MOTION_STATE == "FORWARD":
        A,B,C,D = 3,3,3,3
    if MOTION_STATE == "TURNLEFT1":
        A,B,C,D = 6,0,6,0
    if MOTION_STATE == "TURNRIGHT1":
        A,B,C,D = 0,6,0,6
        
    if MOTION_STATE == "TURNLEFT2":
        A,B,C,D = 5,0,5,0
    if MOTION_STATE == "TURNRIGHT2":
        A,B,C,D = 0,5,0,5
        
    if MOTION_STATE == "TURNLEFT3":
        A,B,C,D = 7,0,7,0
    if MOTION_STATE == "TURNRIGHT3":
        A,B,C,D = 0,7,0,7
   
    print("A B C D",A,B,C,D)
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
   
"""
測試前先調整相機角度 實際80cm處對到刻度80cm處
由上往下改參數 並標記
"""

"""
Update:
pack find_lane(frame) as a function
向下傾斜 Arrow程式要改cropped area
最大視角範圍 大約54cm
Region劃分方式改變
pwm_base 分類
"""
camera_port = 0

Hmin_green, Smin_green, Vmin_green = 35, 80, 46
Hmax_green, Smax_green, Vmax_green = 85, 255, 230

poly_h, poly_w, L = 280, 160, 240  # fixed

deltaHALT, deltaALERT, deltaAUX = 98, 180, 235

R1_threshold, R2_threshold, R3_threshold = 5000, 8000, 10000
L1_threshold, L2_threshold, L3_threshold = 5000, 8000, 10000

pwm_base_normal = 40
pwm_base_slower = 30

R1_delta, R2_delta, R3_delta = 20, 17, 15
L1_delta, L2_delta, L3_delta = 20, 17, 15


def pwmConverter(base,delta):
    if delta > 0:
        direction = 'R'
    elif delta < 0:
        direction = 'L'
    else :
        direction = 'M'
    
    print("pwm base:",base)
    print("pwm delta:",delta)
    pwmR = base - delta
    pwmL = base + delta
    
    return pwmL, pwmR, direction

def find_lane(frame):
    # fileIndex = 10

    # """ read file """
    # path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\findlane"
    # try:
        # img = cv2.imread(path+str(fileIndex)+".jpg")
        # img = cv2.resize(img, (640, 480))
    # except:
        # try:
            # img = cv2.imread(path+str(fileIndex)+".png")
            # img = cv2.resize(img, (640, 480))
        # except:
            # print("Error: non-existent file path")

    img = cv2.resize(frame, (640, 480))
    """ frame mask """
    # create a zero array
    trapezoid_stencil = np.zeros_like(img[:,:,0])

    polygon = np.array([[0,480], [320-poly_w,480-poly_h], [320+poly_w,480-poly_h], [640,480]])

    # fill polygon with gray
    cv2.fillConvexPoly(trapezoid_stencil, polygon, 100)
    #cv2.imshow("gray trapezoid",trapezoid_stencil)

    trapezoid_view = cv2.bitwise_and(img,img,mask=trapezoid_stencil)
    #cv2.imshow("trapezoid view img",trapezoid_view)

    """ mark image """
    marked_img = img.copy()
    marked_img = cv2.cvtColor(marked_img,cv2.COLOR_BGR2HSV)

    cv2.polylines(marked_img,pts=[polygon],isClosed=True,color=(30,120,225),thickness=5) # draw polygon on marked img

    for scale in [(80,-5),(70,15),(60,48),(50,80),(40,125),(30,190),(20,270)]:  # mark each scale
        ycoord = 480-poly_h+scale[1]
        cv2.line(marked_img, (160, ycoord), (480, ycoord), (177, 80, 0), 4)
        cv2.putText(marked_img, str(scale[0]), (300,ycoord+5), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,0), 2, cv2.LINE_AA) 
        
    """ perspective transform """
    original = np.float32([[0,480], [320-poly_w,480-poly_h], [320+poly_w,480-poly_h], [640,480]])
    distorted = np.float32([[320-L,480], [320-L,480-poly_h], [320+L,480-poly_h], [320+L,480]])

    # get transform matrix
    M = cv2.getPerspectiveTransform(original, distorted)
    # apply transformation
    rectangle_view = cv2.warpPerspective(trapezoid_view, M, (640, 480))

    """ show rectangle view """
    trapezoid_stencil = cv2.cvtColor(trapezoid_stencil,cv2.COLOR_GRAY2BGR)
    marked_img = cv2.cvtColor(marked_img,cv2.COLOR_HSV2BGR)

    output1 = cv2.hconcat([img, marked_img])
    output2 = cv2.hconcat([trapezoid_view, rectangle_view])
    output3 = cv2.vconcat([output1,output2])
    output3 = cv2.resize(output3, (640, 480))

    cv2.imshow('perspective transform', output3)


    """ cropping """
    x = 320-L
    y = 480-poly_h
    w = 2*L
    h = poly_h
    cropped_rectangle_view = rectangle_view[y:y+h, x:x+w]
    #cv2.imshow("cropped",cropped_rectangle_view)

    """ thresholding """
    cropped_rectangle_view = cv2.cvtColor(cropped_rectangle_view, cv2.COLOR_BGR2RGB)
    cropped_rectangle_view = cv2.cvtColor(cropped_rectangle_view, cv2.COLOR_RGB2HSV)

    lower_green = np.array([Hmin_green, Smin_green, Vmin_green])
    upper_green = np.array([Hmax_green, Smax_green, Vmax_green])
    mask_green = cv2.inRange(cropped_rectangle_view, lower_green, upper_green)
    #cv2.imshow("green threshold", mask_green)


    """ density histogram """
    gray = mask_green.copy()
    # histogram = np.sum(gray[int(gray.shape[0]/2):,:],axis=0)

    # figure, (ax1,ax2) = plt.subplots(2,1)
    # figure.set_size_inches(5,6)
    # ax1.imshow(gray, cmap='gray')
    # ax1.set_title("Warped Masked Frame")
    # ax2.plot(histogram)
    # ax2.set_title("Density Histogram")
    #plt.show()

    """ plot lines """
    marked = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    marked = cv2.cvtColor(marked,cv2.COLOR_BGR2HSV)
    cv2.line(marked, (L, 0), (L, 480), (0, 0, 100), 3)
    #cv2.putText(marked,"R1",(L+deltaHALT//2,poly_h//2),cv2.FONT_HERSHEY_PLAIN, 1, (177, 100, 200), 1, cv2.LINE_AA)
    cv2.line(marked, (L+deltaHALT, 0), (L+deltaHALT, 480), (177, 100, 200), 2)

    #cv2.putText(marked,"L1",(L-deltaHALT//2,poly_h//2),cv2.FONT_HERSHEY_PLAIN, 1, (177, 100, 200), 1, cv2.LINE_AA)
    cv2.line(marked, (L-deltaHALT, 0), (L-deltaHALT, 480), (40, 10, 140), 2)
    cv2.line(marked, (L+deltaHALT, 0), (L+deltaHALT, 480), (40, 10, 140), 2)

    cv2.line(marked, (L-deltaALERT, 0), (L-deltaALERT, 480), (177, 80, 220), 2)
    cv2.line(marked, (L+deltaALERT, 0), (L+deltaALERT, 480), (177, 80, 220), 2)

    cv2.line(marked, (L-deltaAUX, 0), (L-deltaAUX, 480), (90, 80, 220), 2)
    cv2.line(marked, (L+deltaAUX, 0), (L+deltaAUX, 480), (90, 80, 220), 2)

    cv2.line(marked, (L, 0), (L, 480), (0, 0, 100), 3)
    marked = cv2.cvtColor(marked,cv2.COLOR_HSV2BGR)
    cv2.imshow("marked",marked)

    """ divide into pieces, calculate areas """
    R1_Region = gray[:, L:L+deltaHALT]
    #cv2.imshow("R1",R1_Region)
    R1_White = cv2.countNonZero(R1_Region)
    R1_Total = R1_Region.shape[0]*R1_Region.shape[1]
    R1_Area = int(R1_Total - R1_White)
    print("R1 area:",R1_Area)
    print("R1 threshold:",R1_threshold)

    R2_Region = gray[:, L:L+deltaALERT]
    #cv2.imshow("R2",R2_Region)
    R2_White = cv2.countNonZero(R2_Region)
    R2_Total = R2_Region.shape[0]*R2_Region.shape[1]
    R2_Area = int(R2_Total - R2_White)
    print("R2 area:",R2_Area)
    print("R2 threshold:",R2_threshold)

    R3_Region = gray[:, L:L+deltaAUX]
    #cv2.imshow("R3",R3_Region)
    R3_White = cv2.countNonZero(R3_Region)
    R3_Total = R3_Region.shape[0]*R3_Region.shape[1]
    R3_Area = int(R3_Total - R3_White)
    print("R3 area:",R3_Area)
    print("R3 threshold:",R3_threshold)

    L1_Region = gray[:, L-deltaHALT:L]
    #cv2.imshow("L1",L1_Region)
    L1_White = cv2.countNonZero(L1_Region)
    L1_Total = L1_Region.shape[0]*L1_Region.shape[1]
    L1_Area = int(L1_Total - L1_White)
    print("L1 area:",L1_Area)
    print("L1 threshold:",L1_threshold)

    L2_Region = gray[:, L-deltaALERT:L]
    #cv2.imshow("L2",L2_Region)
    L2_White = cv2.countNonZero(L2_Region)
    L2_Total = L2_Region.shape[0]*L2_Region.shape[1]
    L2_Area = int(L2_Total - L2_White)
    print("L2 area:",L2_Area)
    print("L2 threshold:",L2_threshold)

    L3_Region = gray[:, L-deltaAUX:L]
    #cv2.imshow("L3",L3_Region)
    L3_White = cv2.countNonZero(L3_Region)
    L3_Total = L3_Region.shape[0]*L3_Region.shape[1]
    L3_Area = int(L3_Total - L3_White)
    print("L3 area:",L3_Area)
    print("L3 threshold:",L3_threshold)


    """ determine turn left or right and how much """
    MOTION_STATE = "FORWARD"
    pwm_delta = 0 # +,right -,left
    pwm_base = pwm_base_normal   # deflaut speed, without contacting HALT line

    if R1_Area > R1_threshold and L1_Area > L1_threshold :
        # print("R1, L1 area both > threshold, error!!!!! ")
        # print("R1 area=%d>%d=threshold"%(R1_Area, R1_threshold))
        # print("L1 area=%d>%d=threshold"%(L1_Area, L1_threshold))
        pwm_base = pwm_base_slower   # only decisions made by R1,L1 (between HALT line)
        if R3_Area > L3_Area :
            pwm_delta -= R1_delta
            MOTION_STATE = "TURNLEFT1"
        else:
            pwm_delta += L1_delta
            MOTION_STATE = "TURNRIGHT1"
        print("pwm_delta:", pwm_delta)
        
    elif R1_Area > R1_threshold and L1_Area < L1_threshold :
        pwm_delta -= R1_delta
        pwm_base = pwm_base_slower
        #print("turn Left, R1 area=%d>%d=threshold"%(R1_Area, R1_threshold))
        MOTION_STATE = "TURNLEFT1"
        
    elif R1_Area < R1_threshold and L1_Area > L1_threshold :
        pwm_delta += L1_delta
        pwm_base = pwm_base_slower
        #print("turn Right, L1 area=%d>%d=threshold"%(L1_Area, L1_threshold))
        MOTION_STATE = "TURNRIGHT1"
        
    else :
        if R2_Area > R2_threshold and L2_Area > L2_threshold :
            # print("R2, L2 area both > threshold, error!!!!! ")
            # print("R2 area=%d>%d=threshold"%(R2_Area, R2_threshold))
            # print("L2 area=%d>%d=threshold"%(L2_Area, L2_threshold))
            if R3_Area > L3_Area :
                pwm_delta -= R2_delta
                MOTION_STATE = "TURNLEFT2"
            else:
                pwm_delta += L2_delta
                MOTION_STATE = "TURNRIGHT2"
            
        elif R2_Area > R2_threshold and L2_Area < L2_threshold :
            pwm_delta -= R2_delta
            #print("turn Left, R2 area=%d>%d=threshold"%(R2_Area, R2_threshold))
            MOTION_STATE = "TURNLEFT1"
            
        elif R2_Area < R2_threshold and L2_Area > L2_threshold :
            pwm_delta += L2_delta
            #print("turn Right, L2 area=%d>%d=threshold"%(L2_Area, L2_threshold))
            MOTION_STATE = "TURNRIGHT2"
        
        else :
            if R3_Area > R3_threshold and L3_Area > L3_threshold :
                # print("R3, L3 area both > threshold, error!!!!! ")
                # print("R3 area=%d>%d=threshold"%(R3_Area, R3_threshold))
                # print("L3 area=%d>%d=threshold"%(L3_Area, L3_threshold))
                if R3_Area > L3_Area :
                    pwm_delta -= R3_delta
                    MOTION_STATE = "TURNLEFT3"
                else:
                    pwm_delta += L3_delta
                    MOTION_STATE = "TURNRIGHT3"
                
            elif R3_Area > R3_threshold and L3_Area < L3_threshold :
                pwm_delta -= R3_delta
                #print("turn Left, R3 area=%d>%d=threshold"%(R3_Area, R3_threshold))
                MOTION_STATE = "TURNLEFT1"
                
            elif R3_Area < R3_threshold and L3_Area > L3_threshold :
                pwm_delta += L3_delta
                #print("turn Right, L3 area=%d>%d=threshold"%(L3_Area, L3_threshold))
                MOTION_STATE = "TURNRIGHT1"
                
            else :
                MOTION_STATE = "FORWARD"
                print("No area > threshold, keep going!")
                print("pwm_delta:", pwm_delta)

    """ convert pwm_base, pwm_delta to pwm_L, pwm_R """
    pwm_L, pwm_R, Dir = pwmConverter(pwm_base,pwm_delta)
    print("\npwm L:%d\npwm R:%d\nDir:%sState:%s"%(pwm_L,pwm_R,Dir,MOTION_STATE))
    return pwm_L, pwm_R, MOTION_STATE


cap = cv2.VideoCapture(camera_port) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)

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

countImage = 1
countDirR = 0
countDirL = 0
countDirN = 0

totalDirs = 0
countLess  = 0

while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()
    if countImage == 1:
        print("height:",frame.shape[0],"width:",frame.shape[1],"channel:",frame.shape[2])
        print("Image type:",type(frame))
        
    #print("\ncount:",countImage,'\n')
    #cv2.imshow("original",frame)
    if ret == True:
        #Area, Dir ,Distance= find_arrow(frame)
        pwmL, pwmR, MOTION_STATE = find_lane(frame)
        ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(MOTION_STATE)
        print("pwmL:",pwmL,"\npwmR:",pwmR,"\n\n")
        write_Serial(1,1,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)
        time.sleep(0.1)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            sys.exit()
            break
    else:
        print("Error: no ret")
        break
    
cap.release()
cv2.destroyAllWindows()

ser.close()