import torch
import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F


class CNN_Model(nn.Module):
    # 列出需要那些層
    def __init__(self, classes, fine_tuning=False):
        super(CNN_Model, self).__init__()

        # convolution 1, input_shape = (3, 128, 128)
        # -->(124, 124, 64)
        self.conv_layer1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64,
                            kernel_size=(5, 5), stride=(1, 1)),
            nn.ReLU(),
            # --> (62, 62, 64)
            nn.MaxPool2d(kernel_size=3, stride=2)
        )
        3
        # --> (30, 30, 64)
        self.conv_layer2 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=64,
                             kernel_size=(5, 5), stride=(1, 1), padding='same'),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )

        if fine_tuning:
            for p in self.parameters():
                p.requires_grad = False

        # --> (30, 30, 128)
        self.conv_layer3 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128,
                              kernel_size=(3, 3), stride=(1, 1), padding='same'),
            nn.ReLU(),
            # (14, 14, 128)
            nn.MaxPool2d(kernel_size=3, stride=2)
        )

        self.fc = nn.Linear(14*14*128, 128)
        self.fc_1 = nn.Linear(128, classes)
        self.relu = nn.ReLU(inplace=True)

    def forward(self, x):
        out = self.conv_layer1(x)
        out = self.conv_layer2(out)
        out = self.conv_layer3(out)
        out = torch.flatten(out, 1)
        out = self.fc(out)
        out = self.relu(out)
        out = self.fc_1(out)
        return out


