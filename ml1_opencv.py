import os
import cv2
import numpy 
import random
from typing import List

current_dir = os.getcwd()


def get_image_paths(current_dir : str) -> List[str]:
    image_paths = []
    for root, dirs, files in os.walk(current_dir):
        for file_name in files:
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                image_paths.append(os.path.join(root, file_name))
    return image_paths

def get_shahmatka_from_image(image_path : str , divider_h : int = 10, divider_w : int = 6) -> numpy.ndarray :
    is_color_iamge = 1
    image = cv2.imread(image_path, is_color_iamge)
    if is_color_iamge:
        h, w, c = image.shape
    else:
        h, w = image.shape
    black_h = h // divider_h
    black_w = w // divider_w

    row_starts_with_black = True 
    for row_index in range(divider_h):
        if row_starts_with_black:
            black_index = 0
        else:
            black_index = 1
        for col_index in range(divider_w):
            if black_index % 2 == 0:
                image[
                    row_index * black_h : (row_index + 1) * black_h,
                    col_index * black_w : (col_index + 1) * black_w
                ] *= 0
            black_index += 1
        row_starts_with_black = not row_starts_with_black
    return image

def main():
    image_paths = get_image_paths(os.path.join(current_dir, "test_data"))
    for image_path in image_paths:
        divider_h = random.randint(2, 10)
        divider_w = random.randint(2, 10)
        image_name = os.path.basename(image_path)
        new_image = get_shahmatka_from_image(image_path, divider_h, divider_w)
        cv2.imwrite(os.path.join(current_dir, "out", image_name), new_image)
if __name__ == "__main__":
    main()
