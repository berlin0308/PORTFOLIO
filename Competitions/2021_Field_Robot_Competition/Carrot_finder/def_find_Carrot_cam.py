import cv2
import numpy as np

cap = cv2.VideoCapture(0) #w:640 h:480 for both notebook and camera
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#cap.set(cv2.CAP_PROP_BRIGHTNESS,5)

def find_carrot(frame,least_area,Hmin_orange,Smin_orange,Vmin_orange,Hmax_orange,Smax_orange,Vmax_orange):
    
    """ thresholding """
    cvted_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cvted_img = cv2.cvtColor(cvted_img, cv2.COLOR_RGB2HSV)

    lower_orange = np.array([Hmin_orange, Smin_orange, Vmin_orange])
    upper_orange = np.array([Hmax_orange, Smax_orange, Vmax_orange])
    mask_orange = cv2.inRange(cvted_img, lower_orange, upper_orange)
    #cv2.imshow("orange mask", mask_orange)
    frame_carrot = mask_orange
    
    """ calculate area """
    Area = cv2.countNonZero(mask_orange)
    RegionArea = frame.shape[0]*frame.shape[1]
    Perc = float(Area/RegionArea*100)
    #print(Perc, carrot)
    if Area > least_area:
        return Area, True, frame_carrot
    else:
        return Area, False, frame_carrot

def Find_Carrot(frame):

    Hmin_orange_phase1 = 9
    Smin_orange_phase1 = 43
    Vmin_orange_phase1 = 46
    Hmax_orange_phase1 = 25
    Smax_orange_phase1 = 255
    Vmax_orange_phase1 = 255

    frame = cv2.resize(frame, (640, 480))

    x = 240
    y = 100
    w = 70
    h = 90

    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(180,70,25),thickness=3)

    #cv2.imshow("original",frame)

    """ cropping """
    crop = frame[y:y+h, x:x+w]
    cv2.imshow("cropped",crop)
    carrot_area, carrot, frame_carrot = find_carrot(crop,70,Hmin_orange_phase1,Smin_orange_phase1,Vmin_orange_phase1,Hmax_orange_phase1,Vmax_orange_phase1,Vmax_orange_phase1)

    #cv2.imshow("carrot",frame_carrot)
    return carrot


while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    
    carrot = Find_Carrot(frame)
    print("Carrot?",carrot)
    """ fruit """
    x = 180
    y = 85
    w = 130
    h = 85

    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(20,180,225),thickness=3)

    """ box """
    x = 335
    y = 160
    w = 150
    h = 215
    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(60,120,225),thickness=3)
    
    """ carrot """
    x = 240
    y = 100
    w = 70
    h = 90
    polygon = np.array([[x,y], [x,y+h], [x+w,y+h], [x+w,y]])
    cv2.polylines(frame,pts=[polygon],isClosed=True,color=(180,70,25),thickness=3)
    
    
    
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
