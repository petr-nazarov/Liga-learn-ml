import os
import cv2
import numpy as np
import albumentations as A
from varname.helpers import debug

dataset_path = "output\sportsMOT_volley_light_dataset\player_1"


img = cv2.imread(
    r"c:\cod\datasets\sportsMOT_volley_starter_pack.002\sportsMOT_volley_starter_pack.002\sportsMOT_volley_light_dataset\match_001_short\img1\000001.jpg"
)
print(img.shape)
# img_blur = A.Blur(always_apply=True, blur_limit=12)
# augmentor = A.MotionBlur(always_apply=True, blur_limit=11)
# augmentor = A.RGBShift(
#     r_shift_limit=5, g_shift_limit=50, b_shift_limit=5, always_apply=True
# )
# augmentor = A.RandomBrightnessContrast(always_apply=True)
augmentor = A.Compose(
    [
        A.OneOf(
            [
                A.RandomBrightnessContrast(contrast_limit=0.1, p=0.9),
                A.RGBShift(p=0.8),
            ],
            p=0.9,
        ),
        A.OneOf(
            [
                A.Blur(p=0.3),
                A.MotionBlur(p=0.4),
            ],
            p=0.9,
        ),
        A.OpticalDistortion(distort_limit=0.5, shift_limit=0.5, always_apply=True),
        # A.GridDistortion(always_apply=True),
        # A.ElasticTransform(always_apply=True, alpha=3, sigma=20),
        A.HorizontalFlip(always_apply=True),
    ]
)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_a = augmentor(image=img_rgb)["image"]
img_a_bgr = cv2.cvtColor(img_a, cv2.COLOR_RGB2BGR)
img_out = np.vstack([img, img_a_bgr])
outpath = "output\img_a.jpg"
cv2.imwrite(outpath, img_out)
print(outpath)
