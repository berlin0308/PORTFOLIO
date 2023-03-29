from torchvision import datasets, models, transforms
import torch.utils.data
import torch.nn as nn
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import random
from sklearn.model_selection import StratifiedKFold


"""
從分門別類的data訓練模型(資料夾內有多個以class為開頭命名的資料夾 裡面有該class的照片) 
將做好的model存在saving path
"""

seed_value = 123
torch.cuda.manual_seed(seed_value)
torch.cuda.manual_seed_all(seed_value)
random.seed(seed_value)
np.random.seed(seed_value)


def Makdir(path):

    try:
        os.mkdir(path)
    except:
        pass


def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)  # number of samples
    num_batches = len(dataloader)  # batches per epoch

    model.train()  # Sets the model in training mode.
    epoch_loss, epoch_correct = 0, 0
    # device = torch.device('cuda:0')
    for batch_i, (x, y) in enumerate(dataloader): #第幾個batch, x:image, y:ground truth
        # x, y = x.to(device), y.to(device)  # move data to GPU

        # Compute prediction loss
        pred = model(x) # prediction
        loss = loss_fn(pred, y)

        # Optimization by gradients
        optimizer.zero_grad()  # set prevision gradient to 0
        loss.backward()  # backpropagation to compute gradients
        optimizer.step()  # update model params

        # write to logs
        epoch_loss += loss.item()
        epoch_correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    # return avg loss of epoch, acc of epoch
    return epoch_loss / num_batches, epoch_correct / size


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)  # number of samples
    num_batches = len(dataloader)  # batches per epoch

    model.eval()  # Sets the model in test mode.
    epoch_loss, epoch_correct = 0, 0
    # device = torch.device('cuda:0')
    # No training for test data
    with torch.no_grad():
        for batch_i, (x, y) in enumerate(dataloader):
            # x, y = x.to(device), y.to(device)

            pred = model(x)
            loss = loss_fn(pred, y)

            epoch_loss += loss.item()
            epoch_correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    return epoch_loss / num_batches, epoch_correct / size #loss, accuracy


def training(path, n_epochs, batch_size, LR, saving_path):

    Makdir(saving_path)

    transform = transforms.Compose([transforms.ToTensor()])
    train_data = datasets.ImageFolder(path, transform=transform) #train data: 以資料夾名稱當類別 裡面有該類別(ground truth)的照片

    #print(train_data.class_to_idx) 各個類別和其index
    
    """ 將所有data 分成training set, validation set (8:2) """
    train_size = int(0.8 * len(train_data))
    valid_size = len(train_data) - train_size
    train_data, valid_data = torch.utils.data.random_split(train_data, [train_size, valid_size])

    """ 根據batch size 切分成不同的batch """
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, shuffle=True)
    val_loader = torch.utils.data.DataLoader(valid_data, batch_size=batch_size, shuffle=True)

    min_val_loss = np.inf
    
    

    """ 用pytorch裡的ResNet模型 """
    model = models.resnet18(pretrained=True)  # 6803/2158 #pretrained weight: 參考別人訓練好的權重作為初始
    # print(model)
    
    num_ftrs = model.fc.in_features # 該model fc(full connection全連接層)的in_features:512
    class_num = 100 # 修改fc的output有幾種分類 out_features:100
    model.fc = nn.Linear(num_ftrs, class_num)
    """ deep learning相較於ML 知道有那些feature是重要的 """

    """ 把model丟在GPU上面 """
    # device = torch.device('cuda:0')
    # model.to(device)
    # torch.cuda.set_device(0) #第幾個GPU

    # weight_coef = [1 / (6803 / (6803 + 2158)), 1 / (2158 / (6803 + 2158))]
    # weight = torch.FloatTensor(weight_coef).to(device)
    
    criterion = nn.CrossEntropyLoss() #loss function 
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LR) #LR:Learning rate
    # 優化器: 根據weight,data去優化weight

    for epoch in range(n_epochs):
        print("\r" + "{} / {}".format(epoch + 1, n_epochs), end='')
        ###############
        # train model #
        ###############
        train_loss, train_acc = train(train_loader, model, criterion, optimizer)


        ###############
        # valid model #
        ###############
        val_loss, val_acc = test(val_loader, model, criterion)

        if val_loss < min_val_loss: #要用validation loss最好的
            min_val_loss = val_loss
            temp_model = model
            torch.save(temp_model, saving_path + '/model_best.pth') #model檔名:.pth


if __name__ == "__main__":
    lr, batch = 0.0001, 16

    saving_path = r'C:/Users/BERLIN CHEN/Desktop/DDLAB/ML/1202TrainingTest'
    training(path=r'C:/Users/BERLIN CHEN/Desktop/DDLAB/ML/1202TrainingTest/100 Sports Image Classification/train',
             n_epochs=1,
             batch_size=batch,
             LR=lr,
             saving_path=saving_path)