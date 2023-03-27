import torch
import pandas
import tqdm
import cv2

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

path = "C:\\Users\\BERLIN CHEN\\Desktop\\2021FR\\Photos\\findfruit11.jpg"
frame = cv2.imread(path)
frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)


# Inference
results = model(frame)

# Results
results.print()
results.show()  # or .show()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)
