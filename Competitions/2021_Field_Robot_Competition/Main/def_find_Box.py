
def find_Box(frame):
    
    frame = cv2.resize(frame, (640, 480))

    x = 335
    y = 40
    w = 150
    h = 315
    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(90,120,225),thickness=3)
    cv2.imshow("Find Fruit",frame)
    
    crop = frame[y:y+h, x:x+w]
    cv2.imshow("cropped",crop)
    
    Hmin_blue_phase1 = 80
    Smin_blue_phase1 = 43
    Vmin_blue_phase1 = 46
    Hmax_blue_phase1 = 124
    Smax_blue_phase1 = 255
    Vmax_blue_phase1 = 255
    boxblue_area, BOXBLUE, frame_boxblue = find_boxblue(crop,70,Hmin_blue_phase1,Smin_blue_phase1,Vmin_blue_phase1,Hmax_blue_phase1,Vmax_blue_phase1,Vmax_blue_phase1)
    print("BLUEBOX: ",BOXBLUE,round(boxblue_area,1),'%')
    cv2.imshow("Bluebox",frame_boxblue)
    
    Hmin_red1_phase1 = 0
    Smin_red1_phase1 = 50
    Vmin_red1_phase1 = 20
    Hmax_red1_phase1 = 10
    Smax_red1_phase1 = 255
    Vmax_red1_phase1 = 255
    Hmin_red2_phase1 = 175
    Smin_red2_phase1 = 50
    Vmin_red2_phase1 = 20
    Hmax_red2_phase1 = 180
    Smax_red2_phase1 = 255
    Vmax_red2_phase1 = 255
    boxred_area, BOXRED, frame_boxred = find_boxred(crop,70,Hmin_red1_phase1, Smin_red1_phase1, Vmin_red1_phase1, Hmax_red1_phase1, Smax_red1_phase1, Vmax_red1_phase1, Hmin_red2_phase1, Smin_red2_phase1, Vmin_red2_phase1, Hmax_red2_phase1, Smax_red2_phase1, Vmax_red2_phase1)
    print("REDBOX:  ",BOXRED,round(boxred_area,1),'%')
    cv2.imshow("Redbox",frame_boxred)
    
    
    Hmin_green_phase1 = 35
    Smin_green_phase1 = 70
    Vmin_green_phase1 = 30
    Hmax_green_phase1 = 80
    Smax_green_phase1 = 255
    Vmax_green_phase1 = 255
    boxgreen_area, BOXGREEN, frame_boxgreen = find_boxgreen(crop,6500,Hmin_green_phase1,Smin_green_phase1,Vmin_green_phase1,Hmax_green_phase1,Vmax_green_phase1,Vmax_green_phase1)
    print("GREENBOX:",BOXGREEN,round(boxgreen_area,1),'%')
    cv2.imshow("Greenbox",frame_boxgreen)
    
    countBox = 0
    for fruit in [BOXRED,BOXGREEN,BOXBLUE] :
        if fruit == True:
            countBox += 1

    if countBox == 0:
        print("No fruit is found...")
        return "void"
    elif countBox == 1:
        #print("Only 1 is found")
        if BOXRED == True:
            print("\nOnly BOXRED is found")
            return "BOXRED"
        if BOXGREEN == True:
            print("\nOnly BOXGREEN is found")
            return "BOXGREEN"
        if BOXBLUE == True:
            print("\nOnly BOXBLUE is found")
            return "BOXBLUE"
    elif countBox == 2:
        print("\n2 are found")
        return "void"
    elif countBox == 3:
        print("\n3 are found")
        return "void"
    



def find_boxblue(frame,least_area,Hmin_blue,Smin_blue,Vmin_blue,Hmax_blue,Smax_blue,Vmax_blue):
    
    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_blue = np.array([Hmin_blue, Smin_blue, Vmin_blue])
    upper_blue = np.array([Hmax_blue, Smax_blue, Vmax_blue])
    mask_blue = cv2.inRange(cvted_img, lower_blue, upper_blue)
    #cv2.imshow("blue mask", mask_blue)
    frame_boxblue = mask_blue
    
    """ calculate area """
    Area = cv2.countNonZero(mask_blue)
    RegionArea = frame.shape[0]*frame.shape[1]
    Perc = float(Area/RegionArea*100)
    
    if Perc > least_area:
        return Perc, True, frame_boxblue
    else:
        return Perc, False, frame_boxblue

def find_boxred(frame,least_area,Hmin_red1,Smin_red1,Vmin_red1,Hmax_red1,Smax_red1,Vmax_red1, Hmin_red2,Smin_red2,Vmin_red2,Hmax_red2,Smax_red2,Vmax_red2):

    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
    frame_boxred = mask_red
    
    """ calculate area """
    Area = cv2.countNonZero(mask_red)
    RegionArea = frame.shape[0]*frame.shape[1]
    Perc = float(Area/RegionArea*100)
    
    if Perc > least_area:
        return Perc, True, frame_boxred
    else:
        return Perc, False, frame_boxred
  
def find_boxgreen(frame,least_area,Hmin_green,Smin_green,Vmin_green,Hmax_green,Smax_green,Vmax_green):
    
    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_green = np.array([Hmin_green, Smin_green, Vmin_green])
    upper_green = np.array([Hmax_green, Smax_green, Vmax_green])
    mask_green = cv2.inRange(cvted_img, lower_green, upper_green)
    #cv2.imshow("green mask", mask_green)
    frame_boxgreen = mask_green
    
    """ calculate area """
    Area = cv2.countNonZero(mask_green)
    RegionArea = frame.shape[0]*frame.shape[1]
    Perc = float(Area/RegionArea*100)
    
    if Perc > least_area:
        return Perc, True, frame_boxgreen
    else:
        return Perc, False, frame_boxgreen
    
