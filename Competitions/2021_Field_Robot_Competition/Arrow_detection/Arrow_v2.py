import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

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

approx_convex_const = 5
approx_concave_const = 5

Guassian_ksize = 1

def convex_concave_Test(img,cnt,credit,coef):
    if cv2.isContourConvex(cnt) == True:
        print("the contour is not arrow: convex")
        return False,credit,None,coef,img
    else:
        return True,credit,None,coef,img

def vertices_Test(img,cnt,credit,coef):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
    if len(approx_convex) == 5 :
        return True,credit,None,coef,img
    else :
        return False,credit,None,coef,img

def x_config_Test(img,cnt,credit,coef):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
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
            print("x_config_Test: Right arrow")
            return True,credit,'R',coef,img
        elif deltaE < deltaE2 and deltaW > deltaW2 and deltaE < deltaW :
            print("x_config_Test: Left Arrow")
            return True,credit,'L',coef,img
        else:
            return False,credit,None,coef,img
   
def y_config_Test(img,cnt,credit,coef):
    hull = cv2.convexHull(cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
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
        if deltaN > deltaN2 and deltaS > deltaS2 :
            return True,credit,None,coef,img
        else :
            return False,credit,None,coef,img
   
def M_pos_Test(img,cnt,credit,coef):
    M = cv2.moments(cnt)
    if int(M["m00"]) != 0 :
        Cx = int(M["m10"]/M["m00"])
        Cy = int(M["m01"]/M["m00"])
        cv2.circle(img,(Cx,Cy),4,(110,100,100),-1)
        hull = cv2.convexHull(cnt)
        epslion_unit = 0.01*cv2.arcLength(hull,True)
        approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
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
    thershold = 0.006*img.shape[0]*img.shape[1]
    if area > thershold :
        print("area:",area,"thershold:",thershold)
        return True,credit,None,coef,img
    else :
        print("area:",area,"thershold:",thershold)
        return False,credit,None,coef,img
        
def least_arclength_Test(img,cnt,credit,coef):
    length = cv2.arcLength(cnt,True)
    thershold = 0.15*(img.shape[0]+img.shape[1])
    if length < thershold :
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
            print("find defects")
            return True,credit,None,coef,img
        else:
            return False,credit,None,coef,img
    
    except:
        return False,credit,None,coef,img

def concave_vertices_Test(img,cnt,credit,coef):
    const = 5 
    approx_concave = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True)*const,True)
    print(approx_concave)
    cv2.drawContours(img,[approx_concave],0,(132,100,210),1) # light purple to draw convex approx 
    while True:
        if len(approx_concave) == 7:
            break
        else:
            const += 1
            approx_concave = cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True)*const,True)
        if const >= 1000 :
            break
    if len(approx_concave) == 7:
        for point in range(len(approx_concave)):
                x = approx_concave[point][0][0]
                y = approx_concave[point][0][1]
                cv2.circle(convexImage,(x,y),2,(132,100,210),-1)
                text1 = '(' + str(x) + ',' + str(y) + ')'    
        return True,credit,None,coef,img
    else:
        return False,credit,None,coef,img

def find_range(img,best_cnt):
    hull = cv2.convexHull(best_cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,0.05*cv2.arcLength(cnt,True)*approx_convex_const,True)
    #print(approx_concave_const)
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
    print("x_range:",x_range,"y_range:",y_range)
    cv2.rectangle(img,(xlist[4],ylist[4]),(xlist[0],ylist[0]),(52,200,220),1)
    return img,xlist[4],ylist[4],x_range,y_range
    
path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow6.jpg"
orig = cv2.imread(path)
orig = cv2.resize(orig, (800, 450)) # 16:9
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

""" show process """
cvted_img = cv2.cvtColor(cvted_img,cv2.COLOR_HSV2BGR)
mask_red = cv2.cvtColor(mask_red,cv2.COLOR_GRAY2BGR)
mask_red = cv2.cvtColor(mask_red,cv2.COLOR_BGR2HSV)
cv2.putText(mask_red, "Red mask", (320,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
mask_red = cv2.cvtColor(mask_red,cv2.COLOR_HSV2BGR)
closing = cv2.cvtColor(closing,cv2.COLOR_GRAY2BGR)
closing1 = cv2.cvtColor(closing,cv2.COLOR_BGR2HSV)
cv2.putText(closing1, "Morphology", (280,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
closing1 = cv2.cvtColor(closing1,cv2.COLOR_HSV2BGR)

cannyBGR = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_BGR2HSV)
cv2.putText(cannyBGR, "Canny", (380,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
cannyBGR = cv2.cvtColor(cannyBGR,cv2.COLOR_HSV2BGR)

cropped_mask = cv2.hconcat([cvted_img,mask_red])
morphol_canny = cv2.hconcat([closing1,cannyBGR])
DisplayProcess = cv2.vconcat([cropped_mask,morphol_canny])
cv2.imshow("Process",DisplayProcess)

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
contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
if contours:   
    cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
    print("There are",len(cnt_map),"contours:\n")
    count = 0
    record = 0
    scoreList = []
    best_cnt = cnt_map[0]
    for cnt in cnt_map:
        print("Contour",count,":")
        ifArrow1, credit1, arrowDir1, coef1, contoursImage = convex_concave_Test(contoursImage,cnt,3,0)
        ifArrow2, credit2, arrowDir2, coef2, contoursImage  = vertices_Test(contoursImage,cnt,4,0)
        ifArrow3, credit3, arrowDir3, coef3, contoursImage  = x_config_Test(contoursImage,cnt,2,2)
        ifArrow4, credit4, arrowDir4, coef4, contoursImage  = y_config_Test(contoursImage,cnt,1,0)
        ifArrow5, credit5, arrowDir5, coef5, contoursImage  = M_pos_Test(contoursImage,cnt,1,1)
        ifArrow6, credit6, arrowDir6, coef6, contoursImage  = least_area_Test(contoursImage,cnt,6,0)
        ifArrow7, credit7, arrowDir7, coef7, contoursImage  = least_arclength_Test(contoursImage,cnt,2,0)
        ifArrow8, credit8, arrowDir8, coef8, contoursImage  = convexity_defect_Test(contoursImage,cnt,2,0)
        ifArrow9, credit9, arrowDir9, coef9, contoursImage  = concave_vertices_Test(contoursImage,cnt,10,0)
        ifArrowList = [ifArrow1,ifArrow2,ifArrow3,ifArrow4,ifArrow5,ifArrow6,ifArrow7]
        creditList = [credit1,credit2,credit3,credit4,credit5,credit6,credit7]
        arrowDirList = [arrowDir1,arrowDir2,arrowDir3,arrowDir4,arrowDir5,arrowDir6,arrowDir7]
        coefList = [coef1,coef2,coef3,coef4,coef5,coef6,coef7]
        
        
        if ifArrow2 == True :
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
                
            if score > 11 :   # Well-matched contours: noted in light blue
                hull = cv2.convexHull(cnt)
                epslion_unit = 0.01*cv2.arcLength(hull,True)
                approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
                cv2.drawContours(contoursImage,[approx_convex],0,(90,100,210),2) # light blue to draw convex approx
                cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 2, (90,100,210), 2, cv2.LINE_AA)
            elif score > 8 :   # little-matched contours: noted in light green
                hull = cv2.convexHull(cnt)
                epslion_unit = 0.01*cv2.arcLength(hull,True)
                approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
                cv2.drawContours(contoursImage,[approx_convex],0,(60,100,210),1) # light green to draw convex approx 
                cv2.putText(contoursImage, str(score), (approx_convex[0][0][0],approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (60,100,210), 1, cv2.LINE_AA)
        else:
            score = 0   
            print("no score")
        
        scoreList.append(score)            
        count += 1
    
    """ Conclusion """
    print("\n\n\n--------------------------------------------------------------\n\n\n")
    scoreList = sorted(scoreList,reverse=True)
    print(scoreList,count)
    
    
    """ for the most probable contour, best_cnt """
    
    convexImage = canny.copy()
    convexImage = cv2.cvtColor(convexImage,cv2.COLOR_GRAY2BGR)
    convexImage = cv2.cvtColor(convexImage,cv2.COLOR_BGR2HSV)
    hull = cv2.convexHull(best_cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
    cv2.drawContours(convexImage,[approx_convex],0,(30,100,210),2) # light yellow to draw convex approx 
    for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            y = approx_convex[point][0][1]
            cv2.circle(convexImage,(x,y),4,(30,100,210),-1)
            text1 = '(' + str(x) + ',' + str(y) + ')'
            cv2.putText(convexImage, text1, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (30,100,210), 1, cv2.LINE_AA)
  
    text2 = str(record)
    cv2.putText(contoursImage, text2, (approx_convex[0][0][0]+20,approx_convex[0][0][1]-10), cv2.FONT_HERSHEY_PLAIN, 3, (30,100,210), 4, cv2.LINE_AA)
    cv2.drawContours(contoursImage,[approx_convex],0,(30,100,210),2)
    
    concaveImage = canny.copy()
    concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_GRAY2BGR)
    concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_BGR2HSV)
    while True:
        approx_concave = cv2.approxPolyDP(best_cnt,0.05*cv2.arcLength(cnt,True)*approx_concave_const,True)
        approx_concave_const += 1
        print("approx_concave_const:",approx_concave_const)
        if len(approx_concave) == 7 :
            break
        if approx_concave_const == 100 :
            ("Error: can't find concave 7 points")
            break
    print(approx_concave)
    cv2.drawContours(concaveImage,[approx_concave],0,(132,100,210),2) # light purple to draw concave approx   
    if len(approx_concave) == 7 :
        print("concave points:",len(approx_concave))
        for point in range(len(approx_concave)):
                x = approx_concave[point][0][0]
                y = approx_concave[point][0][1]
                cv2.circle(concaveImage,(x,y),4,(132,100,210),-1)
                text3 = '(' + str(x) + ',' + str(y) + ')'
                cv2.putText(concaveImage, text3, (x-15, y-5), cv2.FONT_HERSHEY_PLAIN, 0.8, (132,100,240), 1, cv2.LINE_AA)
    
    furthercrop = canny.copy()
    furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_GRAY2BGR)
    furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_BGR2HSV)
    furthercrop, x_min, y_min, x_range, y_range = find_range(furthercrop,best_cnt)
    y_start = int(y_min - 0.2* y_range)
    x_start = int(x_min - ((1.4* y_range* 5/3)-x_range)/2)
    furthercrop = furthercrop[y_start:y_start+int(1.4*y_range), x_start:x_start+int(1.4* y_range* 5/3)]
    furthercrop = cv2.resize(furthercrop, (500, 300))
    
    """ Display Result """
    cv2.putText(contoursImage, "Contours", (330,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)
    contoursImage = cv2.cvtColor(contoursImage,cv2.COLOR_HSV2BGR)
    #cv2.imshow("contoursImage",contoursImage) 
    
    cv2.putText(convexImage, "Convex", (340,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
    convexImage = cv2.cvtColor(convexImage,cv2.COLOR_HSV2BGR)
    #cv2.imshow("convexImage",convexImage)  
    
    cv2.putText(concaveImage, "Concave", (330,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA)    
    concaveImage = cv2.cvtColor(concaveImage,cv2.COLOR_HSV2BGR)
    #cv2.imshow("concaveImage",concaveImage)  
    
    cv2.putText(furthercrop, "Furthercrop", (280,280), cv2.FONT_HERSHEY_PLAIN, 2, (30,100,255), 2, cv2.LINE_AA) 
    furthercrop = cv2.cvtColor(furthercrop,cv2.COLOR_HSV2BGR)
    #cv2.imshow("furthercrop",furthercrop)

    Contour_Concave = cv2.hconcat([contoursImage,concaveImage])
    Convex_Furthercrop = cv2.hconcat([convexImage,furthercrop])
    DisplayAll = cv2.vconcat([Contour_Concave, Convex_Furthercrop])
    cv2.imshow("Result",DisplayAll)

cv2.waitKey(0)
cv2.destroyAllWindows()
