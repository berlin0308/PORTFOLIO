import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import serial
import sys
import datetime
import math


"""
Adjust the camera by Main/Camera_Adjust.py
"""

MODE = 'TX2'
#MODE = 'debug'


Critical_frame = 1000

camera_port = 0

Lane_perspec = False   # display perspective transform process
#Lane_perspec = True

Lane_regions = False   # display masked, marked frame
Lane_regions = True

Arrow_process = False  # display arrow detecting process
#Arrow_process = True

print_Lane_detail = False
print_Lane_detail = True

if MODE == 'TX2' :
    serialCom = '/dev/ttyACM0'
    ser = serial.Serial(serialCom, 9600)
    

""" untested """
Hmin_green, Smin_green, Vmin_green = 30, 10, 0
Hmax_green, Smax_green, Vmax_green = 95, 255, 255

poly_h, poly_w, L = 280, 160, 240  # fixed

""" Undetermined """
deltaX1, deltaX2, deltaX3 = 50, 100, 240

R1_threshold = 0.3
L1_threshold = 0.3

pwm_base_normal = 80
pwm_base_slower = 60

R1_delta, R2_delta = 25, 30
L1_delta, L2_delta = 25, 30
 
Hmin_red1 = 0
Smin_red1 = 50
Vmin_red1 = 20
Hmax_red1 = 10
Smax_red1 = 255 
Vmax_red1 = 255

Hmin_red2 = 175
Smin_red2 = 50
Vmin_red2 = 20
Hmax_red2 = 180
Smax_red2 = 255
Vmax_red2 = 255

Guassian_ksize = 1

convex_initial_const = 5  # 5
convex_final_const = 10
concave_initial_const = 1  # 5
concave_final_const = 20   # 7,11,12,13

least_area = 100 # adjust by camera
least_arclength = 20 # adjust by camera

criticalArea = 20

tanA = 0.47 # tan25
tanB = 2.14 # tan65

PNdelta_conv = 40
PNdelta_div = 100





def cnt_convex_approx(cnt,initial_const,final_const):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    const = initial_const # low thershold
    approx = []
    while True :
        approx_convex = cv2.approxPolyDP(hull,epslion_unit*const,True)
        if len(approx_convex) == 5 :
            approx = approx_convex
            #print("\nFind convex contour with 5 vertices")
            #print("convex approx const:",const)
            return True,approx_convex
            break
        if const == final_const : # high thershold
            #print("Can't find convex contour, vertices:",len(approx_convex))
            return None,approx_convex
            break
        const += 1
   
def cnt_concave_approx(cnt,initial_const,final_const):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.001*cv2.arcLength(hull,True)
    const = initial_const # low thershold
    approx = []
    while True :
        approx_concave = cv2.approxPolyDP(cnt,epslion_unit*const,True)
        if len(approx_concave) == 7 :
            approx = approx_concave
            #print("\nFind concave contour with 7 vertices")
            #print("concave approx const:",const)
            return True,approx_concave
            break
        if const == final_const : # high thershold
            #print("Can't find concave contour, vertices:",len(approx_concave))
            return None,approx_concave
            break
        const += 1        
    
    
def convex_concave_Test(cnt,credit):
    if cv2.isContourConvex(cnt) == True:
        #print("the contour is not arrow: convex")
        return False,credit
    else:
        return True,credit

def convexity_defect_Test(cnt,credit):
    try:
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        #print(defects[0])
        if len(defects[0])!=0:
            #print("defects are found")
            return True,credit
        else:
            return False,credit
    
    except:
        return False,credit
         

def convex_vertices_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) == 5 :
        return True,credit
    else :
        return False,credit

def concave_vertices_Test(img,cnt,credit):
    const = 5 
    arrow, approx_concave = cnt_concave_approx(cnt,concave_initial_const,concave_final_const)
    #print(approx_concave)
    cv2.drawContours(img,[approx_concave],0,(132,100,210),1) # light purple to draw convex approx 
    if len(approx_concave) == 7:
        for point in range(len(approx_concave)):
                x = approx_concave[point][0][0]
                y = approx_concave[point][0][1]
                cv2.circle(img,(x,y),2,(132,100,210),-1)
                text1 = '(' + str(x) + ',' + str(y) + ')'    
        return True,credit,img
    else:
        return False,credit,img
        
        
def x_config_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit,'N'
    else:  
        xlist = []
        for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            xlist.append(x)
        xlist = sorted(xlist,reverse=True)
        deltaE = xlist[0] - xlist[1]
        deltaE2 = xlist[1] - xlist[2]
        deltaW = xlist[3] - xlist[4]
        deltaW2 = xlist[2] - xlist[3]
        if deltaE > deltaE2 and deltaW < deltaW2 and deltaE > deltaW :
            #print("x_config_Test: Right arrow")
            return True,credit,'R'
        elif deltaE < deltaE2 and deltaW > deltaW2 and deltaE < deltaW :
            #print("x_config_Test: Left Arrow")
            return True,credit,'L'
        else:
            return False,credit,'N'
   
def y_config_Test(cnt,credit):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit
    else:  
        ylist = []
        for point in range(len(approx_convex)):
            y = approx_convex[point][0][1]
            ylist.append(y)
        ylist = sorted(ylist,reverse=True)
        deltaN = ylist[0] - ylist[1]
        deltaN2 = ylist[1] - ylist[2]
        deltaS = ylist[3] - ylist[4]
        deltaS2 = ylist[2] - ylist[3]
        deltaM = deltaN2 + deltaS2
        if deltaM > deltaN and deltaM > deltaS :
            return True,credit
        else :
            return False,credit
   
    
def least_area_Test(cnt,credit):
    area = abs(cv2.contourArea(cnt,True))
    if area > 100:
        thershold = least_area
    else :
        thershold = 0
        
    if area > thershold :
        #print("area:",area,"thershold:",thershold)
        return True,credit
    else :
        #print("area:",area,"thershold:",thershold)
        return False,credit
        
def least_arclength_Test(cnt,credit):
    length = cv2.arcLength(cnt,True)
    thershold = least_arclength
    if length > thershold :
        #print("length:",length,"thershold:",thershold)
        return True,credit
    else:
        #print("length:",length,"thershold:",thershold)
        return False,credit      
   

def find_range(img,best_cnt):
    arrow, approx_convex = cnt_convex_approx(best_cnt,convex_initial_const,convex_final_const)
    try:
        xlist = []
        ylist = []
        for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            y = approx_convex[point][0][1]
            xlist.append(x)
            ylist.append(y)
        xlist = sorted(xlist,reverse=True)
        ylist = sorted(ylist,reverse=True)
        x_range = xlist[0] - xlist[4]
        y_range = ylist[0] - ylist[4]
        #print("x_range:",x_range,"y_range:",y_range)
        cv2.rectangle(img,(xlist[4],ylist[4]),(xlist[0],ylist[0]),(52,200,220),1)
        return img,xlist[4],ylist[4],x_range,y_range
    except:
        return img,0,0,0,0
    
def HoughLinesAnalysis(focus,lines):
    if lines is not None:
        Plist = []
        Nlist = []
        for i in range(0, len(lines)):
            aline = lines[i][0]
            x1 = aline[0]
            x2 = aline[2]
            y1 = aline[1]
            y2 = aline[3]
            
            # cv2.circle(focus,(x1,y1),6,(132,100,210),-1)  # start point
            # cv2.circle(focus,(x2,y2),6,(172,100,210),-1)  # end point
            
            if x1 != x2 :
                m = -1*(y2-y1)/(x2-x1)
            else :
                m = 1000
               
            if m > -1*tanA and m < tanA :
                #print("Find H line")
                cv2.putText(focus, 'H', ((x1+x2)//2, y1+5), cv2.FONT_HERSHEY_PLAIN, 2, (20,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (20,100,200), 3, cv2.LINE_AA)
            elif m > tanB or m < -1*tanB :
                #print("Find V line")
                cv2.putText(focus, 'V', (x1-20, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (5,100,200), 3, cv2.LINE_AA)
            elif m > tanA and m < tanB :
                #print("Find P line, m=",m)
                cv2.putText(focus, 'P', (x2, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (90,100,200), 3, cv2.LINE_AA)
                startPoint = tuple((x1,y1))
                endPoint = tuple((x2,y2))
                Plist.append(startPoint)
                Plist.append(endPoint)
                #print("Plist append:",startPoint,',',endPoint)
                
            elif m < -1*tanA and m > -1*tanB :
                #print("Find N line, m=",m)
                cv2.putText(focus, 'N', (x2-20, (y1+y2)//2), cv2.FONT_HERSHEY_PLAIN, 2, (70,100,240), 1, cv2.LINE_AA)
                cv2.line(focus, (x1, y1), (x2, y2), (70,100,200), 3, cv2.LINE_AA)
                startPoint = tuple((x1,y1))
                endPoint = tuple((x2,y2))
                Nlist.append(startPoint)
                Nlist.append(endPoint)
                #print("Nlist append:",startPoint,',',endPoint)
            
            # if i == 0:
                # cv2.line(focus, (x1, y1), (x2, y2), (20,100,200), 10, cv2.LINE_AA)
            # if i == 1:
                # cv2.line(focus, (x1, y1), (x2, y2), (30,100,200), 10, cv2.LINE_AA)
            # if i == 2:
                # cv2.line(focus, (x1, y1), (x2, y2), (40,100,200), 10, cv2.LINE_AA)
            # if i == 3:
                # cv2.line(focus, (x1, y1), (x2, y2), (50,100,200), 10, cv2.LINE_AA)
            # if i == 4:
                # cv2.line(focus, (x1, y1), (x2, y2), (60,100,200), 10, cv2.LINE_AA)
            # if i == 5:
                # cv2.line(focus, (x1, y1), (x2, y2), (80,100,200), 10, cv2.LINE_AA)
            # if i == 6:
                # cv2.line(focus, (x1, y1), (x2, y2), (100,100,200), 10, cv2.LINE_AA)
            # if i == 7:
                # cv2.line(focus, (x1, y1), (x2, y2), (120,100,200), 10, cv2.LINE_AA)
            # if i == 8:
                # cv2.line(focus, (x1, y1), (x2, y2), (140,100,200), 10, cv2.LINE_AA)
            # if i == 9:
                # cv2.line(focus, (x1, y1), (x2, y2), (160,100,200), 10, cv2.LINE_AA)
            # if i == 10:
                # cv2.line(focus, (x1, y1), (x2, y2), (175,100,200), 10, cv2.LINE_AA)
        if Plist != [] and Nlist != [] :
            sortedP = sorted(Plist, key = lambda P : P[0],reverse=True)
            sortedN = sorted(Nlist, key = lambda N : N[0],reverse=True)
            #print("sorted Plist:",sortedP)
            #print("sorted Nlist:",sortedN)
            
            Plist_maxx_y = sortedP[0][1]
            Plist_minx_y = sortedP[len(sortedP)-1][1]
            Nlist_maxx_y = sortedN[0][1]
            Nlist_minx_y = sortedN[len(sortedN)-1][1]
            cv2.circle(focus,(sortedN[0][0],Nlist_maxx_y),10,(132,100,210),-1)  # right point
            cv2.circle(focus,(sortedP[0][0],Plist_maxx_y),10,(132,100,210),-1)  # right point
            
            cv2.circle(focus,(sortedN[len(sortedN)-1][0],Nlist_minx_y),10,(172,100,210),-1)  # left point
            cv2.circle(focus,(sortedP[len(sortedP)-1][0],Plist_minx_y),10,(172,100,210),-1)  # left point
          
            Rdelta = abs(Plist_maxx_y - Nlist_maxx_y)
            Ldelta = abs(Plist_minx_y - Nlist_minx_y)
            #print("Rdelta",Rdelta,"Ldelta",Ldelta)
            cv2.putText(focus, "HoughLines", (310,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
            if Rdelta < PNdelta_conv and Ldelta > PNdelta_div :
                #print("HoughLines transform Test: Right Arrow")
                cv2.putText(focus, "result: R", (40,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'R'
            elif Rdelta > PNdelta_div and Ldelta < PNdelta_conv :
                #print("HoughLines transform Test: Left Arrow")
                cv2.putText(focus, "result: L", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'L'
            else :
                cv2.putText(focus, "no result", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA) 
                return focus,'N'
        else:
            #print("Can't find N/P line")
            #print("HoughLines transform Test: None")
            return focus,'N'
    else:
        #print("HoughLines transform Test: None")
        return focus,'N'


def Area2Distance(area):
    x = float(area) 
    dist = 161.12*math.exp(-5*pow(10,-4)*x)
    #dist = float(-2*pow(10,-8)*pow(x,3)+9*pow(10,-5)*pow(x,2)-0.1918*x+204.97)
    return int(dist)
    
    
        
def find_arrow(frame):
    try:
        orig = frame
        orig = cv2.resize(orig, (640, 480))
        #cv2.imshow("original",orig)

        """ cropping """
        x = 100
        y = 0
        w = 440
        h = 480
        cropped = orig[y:y+h, x:x+w]
        #cv2.imshow("cropped",cropped)

        """ thresholding """
        cvted_img = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
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

        """ morphology """
        img = mask_red
        kernel = np.ones((4,4),np.uint8)
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
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_GRAY2BGR)
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_BGR2HSV)
        cv2.putText(mask_red, "Red mask", (320,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        mask_red = cv2.cvtColor(mask_red,cv2.COLOR_HSV2BGR)
        closing = cv2.cvtColor(closing,cv2.COLOR_GRAY2BGR)
        closing1 = cv2.cvtColor(closing,cv2.COLOR_BGR2HSV)
        cv2.putText(closing1, "Morphology", (290,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        closing1 = cv2.cvtColor(closing1,cv2.COLOR_HSV2BGR)

        cannyBGR = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
        cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_BGR2HSV)
        cv2.putText(cannyBGR, "Canny", (380,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_HSV2BGR)

        cropped_mask = cv2.hconcat([cvted_img,mask_red])
        morphol_canny = cv2.hconcat([closing1,cannyBGR])
        DisplayProcess = cv2.vconcat([cropped_mask,morphol_canny])
        # cv2.imshow("Process",DisplayProcess)

        """ find contours, search for the arrow shape one """
        cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_BGR2HSV)
        contoursImage = cvted_img.copy()
        #print(contoursImage.shape[1])
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours:   
            cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
            #print("There are",len(cnt_map),"contours:\n")
            count = 0
            record = 0
            index = 0
            scoreList = []
            best_cnt = cnt_map[0]
            for cnt in cnt_map:
                #print("\n\nContour",count,":")
                ifArrow1, credit1  = convex_concave_Test(cnt,3)
                ifArrow2, credit2  = convexity_defect_Test(cnt,2)
                
                ifArrow3, credit3 = convex_vertices_Test(cnt,6)
                ifArrow4, credit4, contoursImage = concave_vertices_Test(contoursImage,cnt,2)
                
                ifArrow5, credit5, xconfigDir  = x_config_Test(cnt,3)
                ifArrow6, credit6  = y_config_Test(cnt,2)
                
                ifArrow7, credit7  = least_area_Test(cnt,10)
                ifArrow8, credit8 = least_arclength_Test(cnt,4)
                
                ifArrowList = [ifArrow1,ifArrow2,ifArrow3,ifArrow4,ifArrow5,ifArrow6,ifArrow7,ifArrow8]
                creditList = [credit1,credit2,credit3,credit4,credit5,credit6,credit7,credit8]

                
                """ Calculate the score """
                score = 0
                for i in range(len(ifArrowList)):
                    if ifArrowList[i] == True :
                        score += 1*creditList[i]
                
                """ Bonus by heuristics """
                if count <= 5:
                    score += 4 # front contours -> larger area
                    
                if score == record and count < 4:
                    score += 5 # almost the same bonus
                
                """ Best-matched contour """
                #print("score:",score,'\n')         
                if score > record:
                    record = score
                    best_cnt = cnt
                    index = count
                    
                if score > 15 :   # Well-matched contours: noted in light blue
                    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
                    cv2.drawContours(contoursImage,[approx_convex],0,(90,100,210),2) # light blue to draw convex approx
                    cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,210), 2, cv2.LINE_AA)
                elif score > 10 :   # little-matched contours: noted in light green
                    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
                    cv2.drawContours(contoursImage,[approx_convex],0,(60,100,210),1) # light green to draw convex approx 
                    cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (60,100,210), 1, cv2.LINE_AA)
            
                scoreList.append(score)            
                count += 1
            
            """ Conclusion for all contours """
            #print("\n\n\n--------------------------------------------------------------\n\n\n")
            scoreList = sorted(scoreList,reverse=True)
            #print("Candidates:",count,"contours\nScore list:",scoreList)
            #print(best_cnt,record,index)
            
            """ For the most probable contour """
            if Arrow_process == True :
                #print("Best score:",record)
                #print("Index:",index)
                
                arrow, best_approx = cnt_convex_approx(best_cnt,convex_initial_const,concave_final_const)
                if cv2.contourArea(best_approx) > least_area:
                    findArrow = True
                else:
                    findArrow = False
                    
                if record >= 40:
                    probstr = "'definitely'"
                elif record >= 35:
                    probstr = "'probablely'"
                elif record >= 30:
                    probstr = "'likely to'"
                else:
                    probstr = "'perhaps'"

                #print("Score:",record)
                # if findArrow == True:      
                    # print("\nThe arrow is",probstr,"be found\n")
                # if findArrow == False: 
                    # print("\nThe arrow can't be found")
                
            """ All tests result for the most probable contour """ 
            if Arrow_process == True :
                testResultImage = canny.copy()
                ifArrow1, credit1  = convex_concave_Test(cnt,3)
                ifArrow2, credit2  = convexity_defect_Test(cnt,2)
                
                ifArrow3, credit3 = convex_vertices_Test(cnt,6)
                ifArrow4, credit4, testResultImage = concave_vertices_Test(testResultImage,cnt,2)
                
                ifArrow5, credit5, xconfigDir  = x_config_Test(cnt,3)
                ifArrow6, credit6  = y_config_Test(cnt,2)
                
                ifArrow7, credit7  = least_area_Test(cnt,10)
                ifArrow8, credit8 = least_arclength_Test(cnt,4)
                
                # print("\nconvex_concave_Test:",ifArrow1)
                # print("convexity_defect_Test",ifArrow2)
                # print("convex_vertices_Test:",ifArrow3)
                # print("concave_vertices_Test:",ifArrow4)
                # print("x_config_Test:",ifArrow5,"Direction:",xconfigDir)
                # print("y_config_Test:",ifArrow6)
                # print("least_area_Test:",ifArrow7)
                # print("least_arclength_Test:",ifArrow8)
                
            """ Convex approx, show points on convexImage"""
            if Arrow_process == True :
                arrowcheck1, approx_convex = cnt_convex_approx(best_cnt,convex_initial_const,convex_final_const)
                #print("\nArrow convex check:",arrowcheck1)
                #print(approx_convex)
                
                convexImage = canny.copy()
                convexImage = cv2.cvtColor(convexImage,cv2.COLOR_GRAY2BGR)
                convexImage = cv2.cvtColor(convexImage,cv2.COLOR_BGR2HSV)
                cv2.drawContours(convexImage,[approx_convex],0,(30,100,210),2) # light yellow to draw convex approx 
                areaText = "Area:"+str(cv2.contourArea(best_cnt))   #+"  countNonZero:"+str(cv2.countNonZero(cropped))
                #print(areaText)
                cv2.putText(convexImage, areaText, (approx_convex[0][0][0]-180,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
                for point in range(len(approx_convex)):
                        x = approx_convex[point][0][0]
                        y = approx_convex[point][0][1]
                        cv2.circle(convexImage,(x,y),4,(30,100,210),-1)
                        text1 = '(' + str(x) + ',' + str(y) + ')'
                        cv2.putText(convexImage, text1, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (30,100,210), 1, cv2.LINE_AA)
                
            
            """ show the best convex contour on contoursImage """
            if Arrow_process == True :
                text2 = str(record)
                cv2.putText(contoursImage, text2, (approx_convex[0][0][0]+20,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
                cv2.drawContours(contoursImage,[approx_convex],0,(30,100,210),2)
                
            
            """ Concave approx, show points on concaveImage"""
            if Arrow_process == True :
                arrowcheck2, approx_concave = cnt_concave_approx(best_cnt,concave_initial_const,concave_final_const)
                #print("\nArrow concave check:",arrowcheck2)
                #print(approx_concave)
                
                concaveImage = canny.copy()
                concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_GRAY2BGR)
                concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_BGR2HSV)
                cv2.drawContours(concaveImage,[approx_concave],0,(132,100,210),2) # light purple to draw concave approx   
                
                if len(approx_concave) == 7 :
                    #print("concave points:",len(approx_concave))
                    for point in range(len(approx_concave)):
                            x = approx_concave[point][0][0]
                            y = approx_concave[point][0][1]
                            cv2.circle(concaveImage,(x,y),4,(132,100,210),-1)
                            text3 = '(' + str(x) + ',' + str(y) + ')'
                            cv2.putText(concaveImage, text3, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (132,100,240), 1, cv2.LINE_AA)
                
            
            """ further cropping accd. to arrow size """
            furthercrop = canny.copy()
            furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_GRAY2BGR)
            furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_BGR2HSV)
            houghImage = furthercrop.copy()
            furthercrop, x_min, y_min, x_range, y_range = find_range(furthercrop,best_cnt)
            if x_range != 0 and y_range != 0 :
                y_start = int(y_min - 0.2* y_range)
                x_start = int(x_min - ((1.4* y_range* 5/3)-x_range)/2)
                houghImage = houghImage[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
                try:
                    houghImage = cv2.resize(houghImage, (500, 300))
                except:
                    print(houghImage.shape)
                furthercrop = furthercrop[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
                furthercrop = cv2.resize(furthercrop, (500, 300))
            
            """ HoughLines transform after further cropping """   
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_HSV2BGR)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_BGR2GRAY)
            lines = cv2.HoughLinesP(houghImage,rho=1,theta=1*np.pi/180,threshold=30,lines=None, minLineLength=40, maxLineGap=5)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_GRAY2BGR)
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_BGR2HSV)
            
            houghImage,HoughLinesDir = HoughLinesAnalysis(houghImage,lines)
            
            houghImage = cv2.cvtColor(houghImage, cv2.COLOR_HSV2BGR)
            #cv2.imshow("HoughLines",houghImage)
                
            """ Determine the arrow direction """
           
            #print("\nx config Test:",xconfigDir)
            #print("\nHoughLines transform Test:",HoughLinesDir)
            if xconfigDir == 'R' and HoughLinesDir == 'R':
                #print("\nArrow Direction: 'definitely' Right")
                cv2.putText(furthercrop, "'definitely' Right", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)
            if xconfigDir == 'L' and HoughLinesDir == 'L' :
                #print("\nArrow Direction: 'definitely' Left")
                cv2.putText(furthercrop, "'definitely' Left", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)        
            
            if (xconfigDir == 'R' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'R') :
                #print("\nArrow Direction: 'probably' Right")
                cv2.putText(furthercrop, "'probably' Right", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA) 
            if (xconfigDir == 'L' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'L') :
                #print("\nArrow Direction: 'probably' Left")
                cv2.putText(furthercrop, "'probably' Left", (120,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA) 
                
            """ Display Result """
            
            Area = int(cv2.contourArea(best_cnt))
            if Area > 200:
                Distance = Area2Distance(Area)
            else:
                Distance = 999
            
            
            if Arrow_process == True :
                distText = "distance:"+ str(Distance)
                cv2.putText(contoursImage,distText , (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
                cv2.putText(contoursImage, "Contours", (330,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
                contoursImage = cv2.cvtColor(contoursImage,cv2.COLOR_HSV2BGR)
                cv2.imshow("contoursImage",contoursImage) 
                
                cv2.putText(convexImage, "Convex", (350,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
                if xconfigDir == 'R' :
                    cv2.putText(convexImage, "result: R", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)  
                if xconfigDir == 'L' :
                    cv2.putText(convexImage, "result: L", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)   
                else :
                    cv2.putText(convexImage, "no result", (20,280), cv2.FONT_HERSHEY_PLAIN, 2, (5,100,255), 2, cv2.LINE_AA)     
                convexImage = cv2.cvtColor(convexImage,cv2.COLOR_HSV2BGR)
                cv2.imshow("convexImage",convexImage)  
                
                cv2.putText(concaveImage, "Concave", (340,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
                concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_HSV2BGR)
                #cv2.imshow("concaveImage",concaveImage)  
                
                cv2.putText(furthercrop, "Furthercrop", (280,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
                furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_HSV2BGR)
                #cv2.imshow("furthercrop",furthercrop)
                
                # Contour_Concave = cv2.hconcat([contoursImage,concaveImage])
                # Convex_Furthercrop = cv2.hconcat([convexImage,furthercrop])
                # DisplayPrimaryResult = cv2.vconcat([Contour_Concave, Convex_Furthercrop])
                # cv2.imshow("Primary Result",DisplayPrimaryResult)
                
                # Displaytwo = cv2.vconcat([DisplayProcess, DisplayPrimaryResult])
                # Displaytwo = cv2.resize(Displaytwo,(500,600))
                # cv2.imshow("Arrow Detection",Displaytwo)
                
                # DisplayFinalResult1 = cv2.hconcat([contoursImage,convexImage])
                # DisplayFinalResult2 = cv2.hconcat([houghImage,furthercrop])
                # DisplayFinalResult = cv2.vconcat([DisplayFinalResult1, DisplayFinalResult2])
                # cv2.imshow("DisplayFinalResult",DisplayFinalResult)
                
            
            
            if (xconfigDir == 'R' and HoughLinesDir == 'R') or (xconfigDir == 'R' and HoughLinesDir == 'N') or (xconfigDir == 'N' and HoughLinesDir == 'R'):
                return Area , 'R' , Distance
            elif (xconfigDir == 'L' and HoughLinesDir == 'L') or (xconfigDir == 'L' and HoughLinesDir == 'L') or (xconfigDir == 'N' and HoughLinesDir == 'L'):
                return Area , 'L', Distance
            else:
                return Area , 'N', Distance

        else:
            print("No contours")
            return 0,'N',999
            
    except:
        print("Exception: find arrow error")
        return 0,'N',999

    
def find_Arrow_Dir_Result(R,L,N,total):
    try:
        PR = float(R/total)
        PL = float(L/total)
        PN = float(N/total)
        print("\n\n\nTotal",total,"frames are included")
        print("P(R):%0.3f\nP(L):%0.3f\nP(N):%0.3f\n\n"%(PR,PL,PN))
    except:
        PR = 0
        PL = 0
        PN = 0
        
    if PR > PL:
        return 'R'
    elif PL > PR:
        return 'L'
    else:
        return 'R'
    

def MOTION_STATE_LEDs(MOTION_STATE):
    A,B,C,D = 1,1,0,0
    if MOTION_STATE == "FORWARD":
        A,B,C,D = 3,3,3,3  # 直走 Green
    
    if MOTION_STATE == "TURN_LEFT!":  # 小轉 Cyan
        A,B,C,D = 5,0,5,0  
    if MOTION_STATE == "TURN_RIGHT!":
        A,B,C,D = 0,5,0,5
        
    if MOTION_STATE == "TURN_LEFT!!!": # 大轉 Yellow
        A,B,C,D = 6,0,6,0
    if MOTION_STATE == "TURN_RIGHT!!!":
        A,B,C,D = 0,6,0,6
        
        
    print("\nA B   ",A,B)
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


def pwmConverter(base,delta):
    if delta > 0:
        direction = 'R'
    elif delta < 0:
        direction = 'L'
    else :
        direction = 'M'
    
    # print("pwm base:",base)
    # print("pwm delta:",delta)
    pwmR = base - delta
    pwmL = base + delta
    
    return pwmL, pwmR, direction

def find_lane(frame):
    
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
    
    if Lane_perspec == True:
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
    #cv2.putText(marked,"R1",(L+deltaX1//2,poly_h//2),cv2.FONT_HERSHEY_PLAIN, 1, (177, 100, 200), 1, cv2.LINE_AA)
    cv2.line(marked, (L+deltaX1, 0), (L+deltaX1, 480), (177, 100, 200), 2)

    #cv2.putText(marked,"L1",(L-deltaX1//2,poly_h//2),cv2.FONT_HERSHEY_PLAIN, 1, (177, 100, 200), 1, cv2.LINE_AA)
    cv2.line(marked, (L-deltaX1, 0), (L-deltaX1, 480), (40, 10, 140), 2)
    cv2.line(marked, (L+deltaX1, 0), (L+deltaX1, 480), (40, 10, 140), 2)

    cv2.line(marked, (L-deltaX2, 0), (L-deltaX2, 480), (177, 80, 220), 2)
    cv2.line(marked, (L+deltaX2, 0), (L+deltaX2, 480), (177, 80, 220), 2)

    cv2.line(marked, (L-deltaX3, 0), (L-deltaX3, 480), (90, 80, 220), 2)
    cv2.line(marked, (L+deltaX3, 0), (L+deltaX3, 480), (90, 80, 220), 2)

    cv2.line(marked, (L, 0), (L, 480), (0, 0, 100), 3)
    marked = cv2.cvtColor(marked,cv2.COLOR_HSV2BGR)
    # cv2.imshow("marked",marked)
    
    """ divide into pieces, calculate areas """
    R1_Region = gray[:, L+deltaX1:L+deltaX3]
    #cv2.imshow("R1",R1_Region)
    R1_White = cv2.countNonZero(R1_Region)
    R1_Total = R1_Region.shape[0]*R1_Region.shape[1]
    R1_Area = round(float((R1_Total - R1_White) / R1_Total),2)
    if print_Lane_detail == True :
        print("R1 area:",R1_Area)
        print("R1 threshold:",R1_threshold)
        
    L1_Region = gray[:, L-deltaX3:L-deltaX1]
    #cv2.imshow("L1",L1_Region)
    L1_White = cv2.countNonZero(L1_Region)
    L1_Total = L1_Region.shape[0]*L1_Region.shape[1]
    L1_Area = round(float((L1_Total - L1_White) / L1_Total),2)
    if print_Lane_detail == True :
        print("\nL1 area:",L1_Area)
        print("L1 threshold:",L1_threshold)
        
    R2_Region = gray[:, L+deltaX2:L+deltaX3]
    #cv2.imshow("R2",R2_Region)
    R2_White = cv2.countNonZero(R2_Region)
    R2_Total = R2_Region.shape[0]*R2_Region.shape[1]
    R2_Area = round(float((R2_Total - R2_White) / R2_Total),2)
    if print_Lane_detail == True :
        print("R2 area:",R2_Area)



    L2_Region = gray[:, L-deltaX3:L-deltaX2]
    #cv2.imshow("L2",L2_Region)
    L2_White = cv2.countNonZero(L2_Region)
    L2_Total = L2_Region.shape[0]*L2_Region.shape[1]
    L2_Area = round(float((L2_Total - L2_White) / L2_Total),2)
    if print_Lane_detail == True :
        print("L2 area:",L2_Area)
    
    
    """ mark the area """
    cv2.putText(marked, "R1:"+str(R1_Area), (322,240), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
    cv2.putText(marked, "L1:"+str(L1_Area), (60,240), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,0), 2, cv2.LINE_AA) 
    
    cv2.putText(marked, "R2:"+str(R2_Area), (405,270), cv2.FONT_HERSHEY_PLAIN, 1, (90,100,200), 1, cv2.LINE_AA) 
    cv2.putText(marked, "R1:"+str(L2_Area), (27,270), cv2.FONT_HERSHEY_PLAIN, 1, (90,100,0), 1, cv2.LINE_AA) 
    
    if Lane_regions == True :
        cv2.imshow("marked",marked)
    
    """ determine turn left or right and how much """
    MOTION_STATE = "FORWARD"
    pwm_delta = 0 # +,right -,left
    pwm_base = pwm_base_normal   # deflaut speed, without contacting HALT line

    if R1_Area > R1_threshold and L1_Area > L1_threshold :
        if print_Lane_detail == True :
            print("R1, L1 area both > threshold !!!")
        # print("R1 area=%d>%d=threshold"%(R1_Area, R1_threshold))
        # print("L1 area=%d>%d=threshold"%(L1_Area, L1_threshold))
        pwm_base = pwm_base_slower   # only decisions made by R1,L1 (between HALT line)
        if R2_Area > L2_Area :
            pwm_delta -= R1_delta
            MOTION_STATE = "TURN_LEFT!!!"
        else:
            pwm_delta += L1_delta
            MOTION_STATE = "TURN_RIGHT!!!"
       
    elif R1_Area > R1_threshold and L1_Area < L1_threshold :
        pwm_delta -= R1_delta
        pwm_base = pwm_base_slower
        #print("turn Left, R1 area=%d>%d=threshold"%(R1_Area, R1_threshold))
        MOTION_STATE = "TURN_LEFT!!!"
        
    elif R1_Area < R1_threshold and L1_Area > L1_threshold :
        pwm_delta += L1_delta
        pwm_base = pwm_base_slower
        #print("turn Right, L1 area=%d>%d=threshold"%(L1_Area, L1_threshold))
        MOTION_STATE = "TURN_RIGHT!!!"
        
    else :
        MOTION_STATE = "FORWARD"
        if print_Lane_detail == True :
            print("No area > threshold, keep going!")
            print("pwm_delta:", pwm_delta)

    """ convert pwm_base, pwm_delta to pwm_L, pwm_R """
    pwm_L, pwm_R, Dir = pwmConverter(pwm_base,pwm_delta)
    print("\npwm L:%d\npwm R:%d\nDir:%s\nState:%s"%(pwm_L,pwm_R,Dir,MOTION_STATE))
    return pwm_L, pwm_R, MOTION_STATE


cap = cv2.VideoCapture(camera_port) # cap = cv2.VideoCapture(cv2.CAP_DSHOW + camera_port)

if camera_port == 0:   # notebook camera
    cap.set(cv2.CAP_PROP_EXPOSURE,-4)
    cap.set(cv2.CAP_PROP_CONTRAST,2)
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

FINDLANE = True
FINDARROW = False

Observ_Distance = 120
Critical_Distance = 80

countImage = 0 


while cap.isOpened():  # Capture frame-by-frame
    ret, frame = cap.read()
    start = datetime.datetime.now()
    
    if countImage == 1:
        write_Serial(1,1,1,0,0,0,2,2,2,2)
        time.sleep(2)
        write_Serial(1,1,1,0,60,60,3,3,3,3)
        time.sleep(4)
        
    if countImage > Critical_frame:
        FINDARROW = True
    
    #print("\ncount:",countImage,'\n')
    #cv2.imshow("original",frame)
    
    if ret == True:
        print("\n----------","the",countImage,"frame","----------")
        FINDLANE = True
        
        print("FINDARROW:",FINDARROW)
        if FINDARROW == True:
            Area, Dir ,Distance = find_arrow(frame)
            print("\nArea:",Area,"\nDir:",Dir,"\nDistance:",Distance)
            write_Serial(1,1,1,0,60,60,5,5,5,5)
        else:
            Area, Dir ,Distance = 0,0,999
        

        
        if Distance < Observ_Distance and Distance > 55:
            if Distance > Critical_Distance:            
                totalDirs += 1
                if Dir == 'R':
                    countDirR += 1
                if Dir == 'L':
                    countDirL += 1
                if Dir == 'N':
                    countDirN += 1
                if totalDirs % 10 == 0:
                    print("\n\n\ncount:",totalDirs)
                    print("\nR:%0.2f \nL:%0.2f \nN:%0.2f \n\n\n"%(countDirR/totalDirs,countDirL/totalDirs,countDirN/totalDirs))      
            
            if Distance <= Critical_Distance:
                print("\n\nDistance < Critical Distance = ",Critical_Distance)
                print("count Less =",countLess)
                countLess += 1
                FINDLANE = False
                if countLess >= 2:
                    ArrowDirResult = find_Arrow_Dir_Result(countDirR,countDirL,countDirN,totalDirs)
                    print("\n\n\n\n\n\n\n\nStart to turn",ArrowDirResult,"\n\n\n\n\n\n")
                    write_Serial(1,1,1,ArrowDirResult,0,0,0,0,0,0)
                    time.sleep(20)   # Drifting time
                    countDirR,countDirL,countDirN,totalDirs,countLess = 0,0,0,0,0 # zeroing the counters
                        
                        
        print("FINDLANE:",FINDLANE)
        if FINDLANE == False:
            print("Stop finding Lane !!!")

        if FINDLANE == True:
            pwmL, pwmR, MOTION_STATE = find_lane(frame)
            ledA,ledB,ledC,ledD = MOTION_STATE_LEDs(MOTION_STATE)
            write_Serial(1,1,1,0,pwmL,pwmR,ledA,ledB,ledC,ledD)

            
        end = datetime.datetime.now()
        print("process time：", (end - start).microseconds//1000, "ms")
        
        time.sleep(0.8)
        
        countImage += 1
        
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
