import cv2
# import torch
# import h5py as  H
import numpy as np
import scipy.io as sio
import pprint as pp
# import torch.utils.data as data
# import torchvision.transforms.functional as F

gt_path = './mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat'
with open(gt_path, 'rb') as f:
    gt_data = sio.loadmat(f)

# gt_data = sio.loadmat(gt_path)
# print(type (gt_data))
# print(gt_data.keys())
# print(type (gt_data['images']))
# print(gt_data['RELEASE'].annolist())
print(gt_data['RELEASE'].shape)
# pp.pprint(gt_data['RELEASE'])

