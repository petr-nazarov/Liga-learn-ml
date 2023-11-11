import torch
import torchvision
import numpy as np
import cv2
from varname.helpers import debug


def manual_transform_to_tenzor (input_tensor):

    ### 
    # Imread reads  images as HWC 
    # Torch reads images as CHW
    ###
    input_tenzor = input_tenzor.permute(2, 0, 1) # CHW
    input_tenzor = input_tenzor.unsqueeze(0) # 1CHW
    input_tenzor = input_tenzor.to(torch.float32)
    img_min = input_tenzor.min()
    img_max = input_tenzor.max()
    # img_tensor = (img_tensor - img_min) / torch.abs(img_max - img_min)
    input_tenzor = input_tenzor  / 255.0
    return input_tenzor
# torch.manual_seed(420)
# np.random.seed(420)
img_path = './output/snippets/match_001_short/player_0/match_001_short_00_000021_x1_790_y1_443_x2_910_y2_563.jpg';
img = cv2.imread(img_path)
h = img.shape[0]
w = img.shape[1]
c = img.shape[2]
img_tensor = torch.from_numpy(img)
transform = torchvision.transforms.ToTensor()
img_torch_tensor = transform(img)

# debug(img_tensor == img_torch_tensor)
# img_tensor = torch.rand(
#         size = (1, 3, h, w)
#         ).uniform_(-1,1)
# debug(img_tensor)
debug(img_tensor.shape)
# print(type(img_tensor))
# debug(img_tensor.max())
# debug(img_tensor.min())
# debug(torch.__version__)
conv = torch.nn.Conv2d(
    # 3 canal image
    in_channels=3,
    out_channels=16,
    kernel_size=(9,9),
    )
params = conv.weight
debug(params.shape)
# debug(params)
out = conv(img_tensor)
debug(out.shape)

# debug(out)
## Home work 
# 
