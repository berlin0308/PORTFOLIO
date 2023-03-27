import cv2
import numpy as np

cap = cv2.VideoCapture(0) #w:640 h:480 for both notebook and camera
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#cap.set(cv2.CAP_PROP_BRIGHTNESS,5)


while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    
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
