from torchvision import datasets, models, transforms
import torch.utils.data
import torch.nn as nn
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import random


root_path = 'C:/Users/BERLIN CHEN/Desktop/100 Sports Image Classification'

print(os.listdir(root_path))

transform = transforms.Compose([transforms.ToTensor])
train_data = datasets.ImageFolder(root_path + "/train", transform=transform)
print(train_data.class_to_idx)
print(len(train_data.classes))