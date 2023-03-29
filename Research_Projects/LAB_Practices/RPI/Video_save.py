import cv2

cap = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640,  480))
gray = cv2.VideoWriter('gray.mp4', fourcc, 20.0, (640,  480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # 水平上下翻轉影像
    # frame = cv2.flip(frame, 0)
    # write the flipped frame

    out.write(frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    gray.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()