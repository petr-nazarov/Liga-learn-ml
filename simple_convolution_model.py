import os
import torch
from torch import nn
from torch.functional import Tensor
import torch.nn.functional as F
import torchvision
import numpy as np
import cv2
from varname.helpers import debug
from torch_convolution import manual_transform_to_tenzor

class Simple2DConv(nn.Module):
    def __init__(
            self,
            ):
        super().__init__()
        # batch norm  ( statefull )
        self.bn1 = nn.BatchNorm2d(
                num_features=64
                )
        self.bn2 = nn.BatchNorm2d(
                num_features=128
                )
        # svertka (stetfull)
        self.conv1 = nn.Conv2d(
                in_channels=3,
                out_channels=64,
                kernel_size=(5, 5),
                )
        self.conv2 = nn.Conv2d(
                in_channels=64,
                out_channels=128,
                kernel_size=(1, 1),
                )
        # aktivatsiya (stateless)
        self.activation = nn.ReLU()

    def forward(self, x: Tensor): 
        x = self.conv1.forward(x)
        debug(x.shape, prefix='conv1')
        x = self.bn1.forward(x)
        x = self.activation.forward(x)
        x = self.conv2.forward(x)
        debug(x.shape, prefix='conv2')
        x = self.bn2.forward(x)
        x = self.activation.forward(x)
        return x

    

if __name__ == '__main__' : 
    img_path = './output/snippets/match_001_short/player_0/match_001_short_00_000021_x1_790_y1_443_x2_910_y2_563.jpg';

    img = cv2.imread(img_path)
    img_tensor = torch.from_numpy(img)
    # #HWC to [CHW] default and to (0,1)
    # transform = torchvision.transforms.ToTensor()
    # img_torch_tensor = transform(img)

    # #HWC to [CHW] our and to (0,1)
    img_torch_tensor = manual_transform_to_tenzor(img_tensor)

    stupid_conv_model = Simple2DConv()
    debug(img.shape)
    debug(img_torch_tensor.shape)
    out = stupid_conv_model.forward(img_torch_tensor)
    debug(out.shape)
    debug(out[0][15] * 255)

    ## Homework
    ## 16 random chanels form out : visualize and glue 16 of them (4x4)
