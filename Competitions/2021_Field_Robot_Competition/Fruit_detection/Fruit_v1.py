import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import serial



camera_port = 1

path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\findfruit3.jpg"

Hmin_green = 35
Smin_green = 43
Vmin_green = 46
Hmax_green = 77
Smax_green = 255
Vmax_green = 255

Hmin_red2 = 175
Smin_red2 = 50
Vmin_red2 = 20
Hmax_red2 = 180
Smax_red2 = 255
Vmax_red2 = 255

Guassian_ksize = 45
morphol_kernel = 20

def find_lemon(frame):

    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([Hmin_green, Smin_green, Vmin_green])
    upper_green = np.array([Hmax_green, Smax_green, Vmax_green])
    mask_green = cv2.inRange(cvted_img, lower_green, upper_green)
    #cv2.imshow("green mask", mask_green)

    """ Gaussion blur """
    blur = cv2.GaussianBlur(mask_green,(Guassian_ksize,Guassian_ksize),0)
    
    """ morphology """
    img = blur.copy()
    kernel = np.ones((morphol_kernel,morphol_kernel),np.uint8)
    #erosion = cv2.erode(img,kernel,iterations = 1)
    dilation = cv2.dilate(img,kernel,iterations = 1)
    #opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    showMorphology = cv2.hconcat([dilation,closing])
    #cv2.imshow("Morphology",showMorphology)

    """ edge, Canny """
    canny = cv2.Canny(closing, 60, 100)
    #cv2.imshow("Canny",canny)

    """ show Process """
    cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_HSV2BGR)
    mask_green = cv2.cvtColor(mask_green,cv2.COLOR_GRAY2BGR)
    mask_green = cv2.cvtColor(mask_green,cv2.COLOR_BGR2HSV)
    cv2.putText(mask_green, "green mask", (320,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
    mask_green = cv2.cvtColor(mask_green,cv2.COLOR_HSV2BGR)
    closing = cv2.cvtColor(closing,cv2.COLOR_GRAY2BGR)
    closing1 = cv2.cvtColor(closing,cv2.COLOR_BGR2HSV)
    cv2.putText(closing1, "Morphology", (290,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
    closing1 = cv2.cvtColor(closing1,cv2.COLOR_HSV2BGR)

    cannyBGR = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_BGR2HSV)
    houghImage = cannyBGR.copy()
    cv2.putText(cannyBGR, "Canny", (380,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
    cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_HSV2BGR)

    cropped_mask = cv2.hconcat([cvted_img,mask_green])
    morphol_canny = cv2.hconcat([closing1,cannyBGR])
    DisplayProcess = cv2.vconcat([cropped_mask,morphol_canny])
    DisplayProcess = cv2.resize(DisplayProcess,(640,480))
    cv2.imshow("Process",DisplayProcess)
 
    contours, heir = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
    index = 0
    for cnt in cnt_map:
       
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
    
        area = cv2.contourArea(cnt)
        (x, y, w, h) = cv2.boundingRect(approx)
        print("index: {}, original: {}, approx: {}, o/a: {},  w: {}, h: {}, area: {}".format(index, len(cnt), len(approx), str(len(cnt)/len(approx)), w,h,area))
        index += 1
        cv2.drawContours(canny, [approx], 0, (5, 255, 220), 1)
        #cv2.putText(canny, str(index), (x+(w/2), y+(h/2)), cv2.FONT_HERSHEY_SIMPLEX,0.5, (4, 4, 253), 2)
    cv2.imshow("contours",canny)
    
frame = cv2.imread(path)
find_lemon(frame)

cv2.waitKey(0)
# cap = cv2.VideoCapture(camera_port,cv2.CAP_DSHOW) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)

# if camera_port == 0:   # notebook camera
    # #cap.set(cv2.CAP_PROP_EXPOSURE,-4)
    # #cap.set(cv2.CAP_PROP_CONTRAST,0)
    # print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    # print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))
    
# if camera_port == 1:  # usb camera
    # cap.set(cv2.CAP_PROP_EXPOSURE,-7)
    # cap.set(cv2.CAP_PROP_CONTRAST,10)
    # print("Contrast:",cap.get(cv2.CAP_PROP_CONTRAST))
    # print("Exposure:",cap.get(cv2.CAP_PROP_EXPOSURE))

# print("Start capturing video from the camera")

# if cap.isOpened() == False:
    # print("Error: Failed to read the video stream")
# else:
    # print("Read images successfully\n")
 
# countImage = 0
# while cap.isOpened():  # Capture frame-by-frame
    # ret, frame = cap.read()
    # if countImage == 1:
        # print("height:",frame.shape[0],"width:",frame.shape[1],"channel:",frame.shape[2])
        # print("Image type:",type(frame))
        
    # #print("\ncount:",countImage,'\n')
    # cv2.imshow("original",frame)
    # if ret == True:
        # find_lemon(frame)
        # if cv2.waitKey(25) & 0xFF == ord("q"):
            # break
        # countImage += 1
        # time.sleep(0.02)
    # else:
        # print("Error: no ret")
        # break
    

# cap.release()
# cv2.destroyAllWindows()
# ser.close()
    
# except :
    # print("Error: Failed to capture the video")
