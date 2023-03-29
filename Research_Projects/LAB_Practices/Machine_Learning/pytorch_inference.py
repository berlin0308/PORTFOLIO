import torch
from model import CNN_Model
import cv2
from torchvision import transforms
import torch.nn.functional as F
from PIL import Image
import os
import numpy


"模型推論 (Model Inference) 實際上描述的就是模型已經完成訓練與評估，並將模型部署到實際的目標硬體中，將資料輸入到模型中，並由模型預測結果的過程。"


def ResNetPredict(image, model):
    transform = transforms.Compose([transforms.Resize((128, 128)), transforms.ToTensor()]) 
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = transform(image)
    image = image.unsqueeze(0) # [batch size,channels,width,height]
    with torch.no_grad():
        output = model(image)
        # print(output) 各類別多少信心是對的
        # output = F.softmax(output, dim=1)
        score, predicted = torch.max(output, 1) #取最有可能的類別

    return predicted, score, output

model = torch.load("C:/Users/BERLIN CHEN/Desktop/DDLAB/ML/1202TrainingTest/model_best.pth")

image = cv2.imread("C:/Users/BERLIN CHEN/Desktop/DDLAB/ML/1202TrainingTest/100 Sports Image Classification/images to predict/1.jpg")
p,s,out_tensor = ResNetPredict(image, model)
out_numpy = out_tensor.numpy()
print(out_numpy[0][1])

class_list = os.listdir('C:/Users/BERLIN CHEN/Desktop/DDLAB/ML/1202TrainingTest/100 Sports Image Classification/train')
print(class_list)

max = 0.0
max_i = 0
for i,element in enumerate(class_list):
    print(str(i)+": "+element)
    if out_numpy[0][i]>max:
        max = out_numpy[0][i]
        max_i = i

print("\n\nMost probable class:",max_i)
print("Max value:",max)