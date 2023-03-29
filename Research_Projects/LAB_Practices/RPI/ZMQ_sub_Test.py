import cv2
import imagezmq

image_hub = imagezmq.ImageHub(open_port='tcp://*:20009')

while True:
    rpi_name,image = image_hub.recv_image()
    print(rpi_name)
    image_hub.send_reply(b'ok')
    cv2.imshow(rpi_name, image)
    cv2.waitKey(5)