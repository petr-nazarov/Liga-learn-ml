import os
import cv2
import numpy 
from typing import List

current_dir = os.getcwd()


def get_image_paths(current_dir : str) -> List[str]:
    image_paths = []
    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                image_paths.append(os.path.join(root, file_name))
    return image_paths

def get_modified_image(image_path : str) :
    is_color_iamge = 1
    image = cv2.imread(image_path, is_color_iamge)
    if is_color_iamge:
        h, w, c = image.shape
    else:
        h, w = image.shape
    dividers = 9
    black_h = h // dividers 
    black_w = w // dividers

    black_index = 0
    for row_index in range(dividers):
        for col_index in range(dividers):
            if black_index % 2 == 0:
                image[
                    row_index * black_h : (row_index + 1) * black_h,
                    col_index * black_w : (col_index + 1) * black_w
                ] *= 0
            black_index += 1
    return image

def main():
    image_paths = get_image_paths(os.path.join(current_dir, "test_data"))
    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        new_image = get_modified_image(image_path)
        cv2.imwrite(os.path.join(current_dir, "out", image_name), new_image)
main()
