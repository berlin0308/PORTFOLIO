import imagezmq
import cv2

sender = imagezmq.ImageSender(connect_to='tcp://140.112.94.129:20009')

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    print("OK")
    if ret:
        sender.send_image("Berlin", frame)
