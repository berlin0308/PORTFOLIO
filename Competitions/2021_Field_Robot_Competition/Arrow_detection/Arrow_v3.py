import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

camera_port = 1

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

least_area_const = 0.01 # adjust by camera
least_arclength_const = 0.15 # adjust by camera

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
    
def convex_concave_Test(img,cnt,credit,coef):
    if cv2.isContourConvex(cnt) == True:
        print("the contour is not arrow: convex")
        return False,credit,None,coef,img
    else:
        return True,credit,None,coef,img

def convex_vertices_Test(img,cnt,credit,coef):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) == 5 :
        return True,credit,None,coef,img
    else :
        return False,credit,None,coef,img

def x_config_Test(img,cnt,credit,coef):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit,None,coef,img
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
            return True,credit,'R',coef,img
        elif deltaE < deltaE2 and deltaW > deltaW2 and deltaE < deltaW :
            #print("x_config_Test: Left Arrow")
            return True,credit,'L',coef,img
        else:
            return False,credit,None,coef,img
   
def y_config_Test(img,cnt,credit,coef):
    arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
    if len(approx_convex) != 5:
        return False,credit,None,coef,img
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
            return True,credit,None,coef,img
        else :
            return False,credit,None,coef,img
   
def M_pos_Test(img,cnt,credit,coef):
    M = cv2.moments(cnt)
    if int(M["m00"]) != 0 :
        Cx = int(M["m10"]/M["m00"])
        Cy = int(M["m01"]/M["m00"])
        cv2.circle(img,(Cx,Cy),4,(110,100,100),-1)
        arrow, approx_convex = cnt_convex_approx(cnt,convex_initial_const,convex_final_const)
        if len(approx_convex) != 5:
            return False,credit,None,coef,img
        else:  
            xlist = []
            ylist = []
            for point in range(len(approx_convex)):
                x = approx_convex[point][0][0]
                y = approx_convex[point][0][1]
                xlist.append(x)
                ylist.append(y)
            x_max = max(xlist)
            x_min = min(xlist)
            y_max = max(ylist)
            y_min = min(ylist)
            d = 2*cv2.arcLength(cnt,True)
            error = math.sqrt(((x_max + x_min)/2)**2 + ((y_max + y_min)/2)**2)
            if error < d :
                #print(error,d)
                return True,credit,None,coef,img
            else :
                #print(error,d)
                return False,credit,None,coef,img
    else:
        return False,credit,None,coef,img
 
def least_area_Test(img,cnt,credit,coef):
    area = abs(cv2.contourArea(cnt,True))
    thershold = least_area_const*img.shape[0]*img.shape[1]
    if area > thershold :
        print("area:",area,"thershold:",thershold)
        return True,credit,None,coef,img
    else :
        print("area:",area,"thershold:",thershold)
        return False,credit,None,coef,img
        
def least_arclength_Test(img,cnt,credit,coef):
    length = cv2.arcLength(cnt,True)
    thershold = least_arclength_const*(img.shape[0]+img.shape[1])
    if length > thershold :
        print("length:",length,"thershold:",thershold)
        return True,credit,None,coef,img
    else:
        print("length:",length,"thershold:",thershold)
        return False,credit,None,coef,img      
   
def convexity_defect_Test(img,cnt,credit,coef):
    try:
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        #print(defects[0])
        if len(defects[0])!=0:
            print("defects are found")
            return True,credit,None,coef,img
        else:
            return False,credit,None,coef,img
    
    except:
        return False,credit,None,coef,img

def concave_vertices_Test(img,cnt,credit,coef):
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
        return True,credit,None,coef,img
    else:
        return False,credit,None,coef,img

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
    
def find_arrow(frame):
    # path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow7.jpg"
    # orig = cv2.imread(path)
    orig = cv2.resize(frame, (800, 450)) # 16:9
    #cv2.imshow("original",orig)

    """ cropping """
    x = 150
    y = 100
    w = 500
    h = 300
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

    """ HoughLines transform """
    # copy = canny.copy()
    # copy = cv2.cvtColor(copy, cv2.COLOR_GRAY2BGR)
    # copy = cv2.cvtColor(copy, cv2.COLOR_BGR2HSV)
    # lines = cv2.HoughLinesP(canny,rho=1,theta=np.pi/180,threshold=60)
    # if lines is not None:
            # for i in range(0, len(lines)):
                # l = lines[i][0]
                # cv2.line(copy, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    # copy = cv2.cvtColor(copy, cv2.COcvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_HSV2BGR)LOR_HSV2BGR)
    # cv2.imshow("HoughLines",copy)

    """ find contours, search for the arrow shape one """
    cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_BGR2HSV)
    contoursImage = cvted_img.copy()
    print(contoursImage.shape[1])
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if contours:   
        cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
        print("There are",len(cnt_map),"contours:\n")
        count = 0
        record = 0
        index = 0
        scoreList = []
        best_cnt = cnt_map[0]
        for cnt in cnt_map:
            print("\n\nContour",count,":")
            ifArrow1, credit1, arrowDir1, coef1, contoursImage = convex_concave_Test(contoursImage,cnt,3,0)
            ifArrow2, credit2, arrowDir2, coef2, contoursImage  = convex_vertices_Test(contoursImage,cnt,4,0)
            ifArrow3, credit3, arrowDir3, coef3, contoursImage  = x_config_Test(contoursImage,cnt,2,2)
            ifArrow4, credit4, arrowDir4, coef4, contoursImage  = y_config_Test(contoursImage,cnt,1,0)
            ifArrow5, credit5, arrowDir5, coef5, contoursImage  = M_pos_Test(contoursImage,cnt,1,1)
            ifArrow6, credit6, arrowDir6, coef6, contoursImage  = least_area_Test(contoursImage,cnt,6,0)
            ifArrow7, credit7, arrowDir7, coef7, contoursImage  = least_arclength_Test(contoursImage,cnt,2,0)
            ifArrow8, credit8, arrowDir8, coef8, contoursImage  = convexity_defect_Test(contoursImage,cnt,2,0)
            ifArrow9, credit9, arrowDir9, coef9, contoursImage  = concave_vertices_Test(contoursImage,cnt,10,0)
            ifArrowList = [ifArrow1,ifArrow2,ifArrow3,ifArrow4,ifArrow5,ifArrow6,ifArrow7,ifArrow8,ifArrow9]
            creditList = [credit1,credit2,credit3,credit4,credit5,credit6,credit7,credit8,credit9]
            arrowDirList = [arrowDir1,arrowDir2,arrowDir3,arrowDir4,arrowDir5,arrowDir6,arrowDir7,arrowDir8,arrowDir9]
            coefList = [coef1,coef2,coef3,coef4,coef5,coef6,coef7,coef8,coef9]
            
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
            print("score:",score,'\n')         
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
        print("\n\n\n--------------------------------------------------------------\n\n\n")
        scoreList = sorted(scoreList,reverse=True)
        print("Candidate contours:",count,"\nScore list:",scoreList)
        #print(best_cnt,record,index)
        
        """ For the most probable contour """
        print("Best score:",record)
        print("Index:",index)
        
        arrow, best_approx = cnt_convex_approx(best_cnt,convex_initial_const,concave_final_const)
        if cv2.contourArea(best_approx) > least_area_const*img.shape[0]*img.shape[1] :
            findArrow = True
        else:
            findArrow = False
        print("\nIf the arrow is found:",findArrow)
        
        """ All tests result for the most probable contour """ 
        testResultImage = canny.copy()
        ifArrow1, credit1, arrowDir1, coef1, testResultImage = convex_concave_Test(testResultImage,best_cnt,3,0)
        ifArrow2, credit2, arrowDir2, coef2, testResultImage  = convex_vertices_Test(testResultImage,best_cnt,4,0)
        ifArrow3, credit3, arrowDir3, coef3, testResultImage  = x_config_Test(testResultImage,best_cnt,2,2)
        ifArrow4, credit4, arrowDir4, coef4, testResultImage  = y_config_Test(testResultImage,best_cnt,1,0)
        ifArrow5, credit5, arrowDir5, coef5, testResultImage  = M_pos_Test(testResultImage,best_cnt,1,1)
        ifArrow6, credit6, arrowDir6, coef6, testResultImage  = least_area_Test(testResultImage,best_cnt,10,0)
        ifArrow7, credit7, arrowDir7, coef7, testResultImage  = least_arclength_Test(testResultImage,best_cnt,4,0)
        ifArrow8, credit8, arrowDir8, coef8, testResultImage  = convexity_defect_Test(testResultImage,best_cnt,2,0)
        ifArrow9, credit9, arrowDir9, coef9, testResultImage  = concave_vertices_Test(testResultImage,best_cnt,3,0)
        print("\nconvex_concave_Test:",ifArrow1)
        print("convex_vertices_Test",ifArrow2)
        print("x_config_Test:",ifArrow3)
        print("y_config_Test:",ifArrow4)
        print("M_pos_Test:",ifArrow5)
        print("least_area_Test:",ifArrow6)
        print("least_arclength_Test:",ifArrow7)
        print("convexity_defect_Test:",ifArrow8)
        print("concave_vertices_Test:",ifArrow9)
        
        """ Convex approx, show points on convexImage"""
        arrowcheck1, approx_convex = cnt_convex_approx(best_cnt,convex_initial_const,convex_final_const)
        print("\nArrow convex check:",arrowcheck1)
        print(approx_convex)
        
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
        text2 = str(record)
        cv2.putText(contoursImage, text2, (approx_convex[0][0][0]+20,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
        cv2.drawContours(contoursImage,[approx_convex],0,(30,100,210),2)
        
        
        """ Concave approx, show points on concaveImage"""
        arrowcheck2, approx_concave = cnt_concave_approx(best_cnt,concave_initial_const,concave_final_const)
        print("\nArrow concave check:",arrowcheck2)
        print(approx_concave)
        
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
        furthercrop, x_min, y_min, x_range, y_range = find_range(furthercrop,best_cnt)
        if x_range != 0 and y_range != 0 :
            y_start = int(y_min - 0.2* y_range)
            x_start = int(x_min - ((1.4* y_range* 5/3)-x_range)/2)
            furthercrop = furthercrop[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
            furthercrop = cv2.resize(furthercrop, (500, 300))
            
        """ Determine the arrow direction """
        a,b,Arrowdir,d,contoursImage = x_config_Test(contoursImage,best_cnt,2,2)
        if Arrowdir == 'R' :
            print("\nArrow Direction: Right")
            cv2.putText(furthercrop, "Right Arrow", (160,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)
        if Arrowdir == 'L' :
            print("\nArrow Direction: Left")
            cv2.putText(furthercrop, "Left Arrow", (160,40), cv2.FONT_HERSHEY_PLAIN, 2, (52,200,220), 2, cv2.LINE_AA)        
            
        """ Display Result """
        cv2.putText(contoursImage, "Contours", (330,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
        contoursImage = cv2.cvtColor(contoursImage,cv2.COLOR_HSV2BGR)
        #cv2.imshow("contoursImage",contoursImage) 
        
        cv2.putText(convexImage, "Convex", (350,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
        convexImage = cv2.cvtColor(convexImage,cv2.COLOR_HSV2BGR)
        #cv2.imshow("convexImage",convexImage)  
        
        cv2.putText(concaveImage, "Concave", (340,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
        concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_HSV2BGR)
        #cv2.imshow("concaveImage",concaveImage)  
        
        cv2.putText(furthercrop, "Furthercrop", (280,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
        furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_HSV2BGR)
        #cv2.imshow("furthercrop",furthercrop)

        Contour_Concave = cv2.hconcat([contoursImage,concaveImage])
        Convex_Furthercrop = cv2.hconcat([convexImage,furthercrop])
        DisplayResult = cv2.vconcat([Contour_Concave, Convex_Furthercrop])
        #cv2.imshow("Result",DisplayResult)
        
        DisplayALL = cv2.vconcat([DisplayProcess, DisplayResult])
        DisplayALL = cv2.resize(DisplayALL,(500,600))
        cv2.imshow("Arrow Detection",DisplayALL)


try:
    cap = cv2.VideoCapture(camera_port, cv2.CAP_DSHOW)
    print("Start capturing video from the camera")
    
    if cap.isOpened() == False:
        print("Error: Failed to read the video stream")
    else:
        print("Read images successfully\n")
    
    countImage = 0
    while cap.isOpened():  # Capture frame-by-frame
        ret, frame = cap.read()
        if countImage == 0:
            print("height:",frame.shape[0],"width:",frame.shape[1],"channel:",frame.shape[2])
            print("Image type:",type(frame))
        #print("count:",countImage)
        cv2.imshow("original",frame)
        if ret == True:
            find_arrow(frame)
           
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
            countImage += 1
        # Break the loop
        else:
            break
        
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()
    
except:
    print("Error: Failed to capture the video")
