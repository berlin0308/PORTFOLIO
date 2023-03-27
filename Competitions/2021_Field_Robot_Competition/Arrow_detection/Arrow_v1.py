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

Hmin_white = 20
Smin_white = 0
Vmin_white = 50
Hmax_white = 255
Smax_white = 255
Vmax_white = 255

approx_convex_const = 5
approx_concave_const = 1

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
        
path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\red_arrow3.jpg"
orig = cv2.imread(path)
orig = cv2.resize(orig, (800, 450)) # 16:9
#cv2.imshow("original",orig)

""" cropping """
x = 150
y = 100
w = 500
h = 300
cropped = orig[y:y+h, x:x+w]
cv2.imshow("cropped",cropped)

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
canny = cv2.Canny(img, 60, 100)
cv2.imshow("Canny",canny)

""" HoughLines transform """
# copy = canny.copy()
# copy = cv2.cvtColor(copy, cv2.COLOR_GRAY2BGR)
# copy = cv2.cvtColor(copy, cv2.COLOR_BGR2HSV)
# lines = cv2.HoughLinesP(canny,rho=1,theta=np.pi/180,threshold=60)
# if lines is not None:
        # for i in range(0, len(lines)):
            # l = lines[i][0]
            # cv2.line(copy, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
# copy = cv2.cvtColor(copy, cv2.COLOR_HSV2BGR)
# cv2.imshow("HoughLines",copy)

""" find contours, search for the arrow shape one """
convexImage = cvted_img.copy()
contours, hierarchy = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
if contours:   
    cnt_map = sorted(contours,key=cv2.contourArea,reverse=True)
    print("There are",len(cnt_map),"contours:\n")
    count = 0
    record = 0
    for cnt in cnt_map:
        print("Contour",count,":")
        ifArrow1, credit1, arrowDir1, coef1, convexImage = convex_concave_Test(convexImage,cnt,3,0)
        ifArrow2, credit2, arrowDir2, coef2, convexImage  = vertices_Test(convexImage,cnt,4,0)
        ifArrow3, credit3, arrowDir3, coef3, convexImage  = x_config_Test(convexImage,cnt,2,2)
        ifArrow4, credit4, arrowDir4, coef4, convexImage  = y_config_Test(convexImage,cnt,1,0)
        ifArrow5, credit5, arrowDir5, coef5, convexImage  = M_pos_Test(convexImage,cnt,1,1)
        ifArrow6, credit6, arrowDir6, coef6, convexImage  = least_area_Test(convexImage,cnt,6,1)
        ifArrow7, credit7, arrowDir7, coef7, convexImage  = least_arclength_Test(convexImage,cnt,2,1)
        #ifArrow7, credit7, arrowDir7, coef7, convexImage  = least_arclength_Test(convexImage,cnt,2,1)
        
        ifArrowList = [ifArrow1,ifArrow2,ifArrow3,ifArrow4,ifArrow5,ifArrow6,ifArrow7]
        creditList = [credit1,credit2,credit3,credit4,credit5,credit6,credit7]
        arrowDirList = [arrowDir1,arrowDir2,arrowDir3,arrowDir4,arrowDir5,arrowDir6,arrowDir7]
        coefList = [coef1,coef2,coef3,coef4,coef5,coef6,coef7]
       
        score = 0
        for i in range(len(ifArrowList)):
            if ifArrowList[i] == True :
                score += 1*creditList[i]
        if count <= 5:
            score += 4 # front contours -> larger area
            
        if score == record and count < 4:
            score += 5 # almost the same bonus
            
        print(score,'\n')         
        if score > record:
            record = score
            best_cnt = cnt   
            
        if score > 11 :
            hull = cv2.convexHull(cnt)
            epslion_unit = 0.01*cv2.arcLength(hull,True)
            approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
            cv2.drawContours(convexImage,[approx_convex],0,(90,100,210),2) # light blue to draw convex approx
        elif score > 8 :
            hull = cv2.convexHull(cnt)
            epslion_unit = 0.01*cv2.arcLength(hull,True)
            approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
            cv2.drawContours(convexImage,[approx_convex],0,(60,100,210),1) # light green to draw convex approx 
        count += 1
        
    hull = cv2.convexHull(best_cnt)
    epslion_unit = 0.01*cv2.arcLength(hull,True)
    approx_convex = cv2.approxPolyDP(hull,epslion_unit*approx_convex_const,True)
    cv2.drawContours(convexImage,[approx_convex],0,(30,100,210),3) # light yellow to draw convex approx 
    for point in range(len(approx_convex)):
            x = approx_convex[point][0][0]
            y = approx_convex[point][0][1]
            cv2.circle(convexImage,(x,y),4,(60,100,0),-1)
            text = '(' + str(x) + ',' + str(y) + ')'
            cv2.putText(convexImage, text, (x-5, y+10), cv2.FONT_HERSHEY_PLAIN, 0.8, (60,100,0), 1, cv2.LINE_AA)
            
    convexImage = cv2.cvtColor(convexImage,cv2.COLOR_HSV2BGR)
    cv2.imshow("convexImage",convexImage)            

cv2.waitKey(0)
cv2.destroyAllWindows()
